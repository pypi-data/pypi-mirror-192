import inspect
import sys
from argparse import ArgumentParser




class ParameterError(Exception):
    pass




def from_object(
    obj,
    *,
    add_help, 
    return_details=None,
):
    if callable(obj):
        return from_callable(
            obj,
            add_help=add_help,
            return_details=return_details,
        )
        #parser.add_argument('--errorlog', '-e', type=dt.ErrorLog)
    parser = ArgumentParser(add_help=add_help)
    subparsers = parser.add_subparsers(dest=obj._dest, required=True)
    for n, m in inspect.getmembers(obj):
        if n.startswith('_'):
            continue
        parent = from_object(
            m, 
            add_help=True,
            return_details=return_details,
        )
        info = dict()
        if not inspect.isfunction(m):
            if hasattr(m, '_aliases'):
                info['aliases'] = m._aliases
        subparser = subparsers.add_parser(
            n.replace('_', '-'), 
            description=parent.description,
            parents=[parent],
            add_help=False,
            **info,
        )
    parser.description = obj.__doc__
    return parser


def from_callable(
    obj, 
    *,
    add_help,
    return_details=None,
):
    if not callable(obj):
        raise TypeError()
    signature = inspect.signature(obj)
    parents = [from_parameter(parameter, add_help=False) for parameter_name, parameter in signature.parameters.items()]
    if signature.return_annotation is not inspect.Signature.empty:
        parents.append(
            from_details(
                default=signature.return_annotation('-'),
                add_help=False,
                type=signature.return_annotation,
                **return_details,
            )
        )
    parser = ArgumentParser(
        parents=parents,
    )
    parser.description = obj.__doc__
    return parser

    
def from_parameter(parameter, *, add_help):
    if type(parameter) is not inspect.Parameter:
        raise TypeError()
    if parameter.name.startswith('_'):
        raise ValueError(parameter.name)
    if parameter.kind is inspect.Parameter.VAR_KEYWORD:
        return from_iterable(parameter.annotation, add_help=add_help)
    annotation = parameter.annotation
    if annotation is inspect.Parameter.empty:
        annotation = dict()
    else:
        annotation = dict(annotation)
    details = dict()
    details['dest'] = parameter.name
    if parameter.kind is inspect.Parameter.POSITIONAL_ONLY:
        if parameter.default is not inspect.Parameter.empty:
            details['nargs'] = '?'
            details['default'] = parameter.default
    elif parameter.kind is inspect.Parameter.VAR_POSITIONAL:
        details['nargs'] = '*'
    elif parameter.kind is inspect.Parameter.KEYWORD_ONLY:
        if 'option_strings' not in annotation.keys():
            annotation['option_strings'] = ['-' + parameter.name.replace('_', '-')]
        if parameter.default is inspect.Parameter.empty:
            details['required'] = True
        else:
            details['required'] = False
            details['default'] = parameter.default
    else:
        raise ParameterError(f"The parameter {parameter.name} is of an unsupported kind. ")
    return from_details(**details, **annotation, add_help=add_help)


def from_iterable(iterable, *, add_help):
    try:
        x = dict(iterable)
    except ValueError:
        x = None
    parents = list()
    if x is None:
        x = list(iterable)
        for v in x:
            parents.append(from_details(**dict(v), add_help=False))
    else:
        for k, v in x.items():
            parents.append(from_details(**dict(v), add_help=False, dest=k))
    return ArgumentParser(
        add_help=add_help,
        parents=parents,
    )


def from_details(*, add_help, option_strings=[], **kwargs):
    parser = ArgumentParser(add_help=add_help)
    parser.add_argument(*option_strings, **kwargs)
    return parser
















