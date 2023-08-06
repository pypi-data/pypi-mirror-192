import contextlib
import tempfile
import inspect
import os


class ExecFunc:
    class Error(Exception):
        pass
    def __init__(self, func, return_dest='outfile'):
        self._func = func
        self._return_dest = return_dest
    def __call__(self, kwargs):
        kwargs = dict(kwargs)
        signature = inspect.signature(self._func)
        args = list()
        for parameter_name, parameter in signature.parameters.items():
            if parameter.kind is inspect.Parameter.POSITIONAL_ONLY:
                args.append(kwargs.pop(parameter.name))
            elif parameter.kind is inspect.Parameter.VAR_POSITIONAL:
                args.extend(kwargs.pop(parameter.name))
        if signature.return_annotation is inspect.Signature.empty:
            assert self._return_dest not in kwargs.keys()
            outstream = None
        else:
            outstream = kwargs.pop(self._return_dest)

        with tempfile.TemporaryDirectory() as tmpdir:
            stdoutdump = os.path.join(tmpdir, 'stdoutdump.txt')
            with open(stdoutdump, 'w') as stdoutstream:
                with contextlib.redirect_stdout(stdoutstream):
                    results = self._func(*args, **kwargs)
            with open(stdoutdump, 'r') as stdoutstream:
                stdouttext = stdoutstream.read()
                if stdouttext != "":
                    raise ExecFunc.Error("The heart of the program wrote something to stdout: \n" + stdouttext)
        if outstream is None:
            if results is not None:
                raise ExecFunc.Error()
        else:
            outstream.write(results, overwrite=True)


