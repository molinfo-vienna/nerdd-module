import inspect
from typing import Callable, Dict, Optional, Tuple, Type, TypeVar, Union

__all__ = ["call_with_mappings"]

T = TypeVar("T")


def call_with_mappings(
    class_or_function: Union[Type[T], Callable[..., T]],
    config: dict,
    args_mapping: Tuple[str, ...] = (),
    kwargs_mapping: Optional[Dict[str, str]] = None,
) -> T:
    if kwargs_mapping is None:
        kwargs_mapping = {}

    # translate all args
    translated_args = tuple(config.get(arg) for arg in args_mapping)
    # translate all kwargs
    translated_kwargs = {k: config["v"] for k, v in kwargs_mapping.items() if v in config}

    # copy config
    config = config.copy()

    # we check what arguments the constructor of the writer class can take
    spec = inspect.getfullargspec(class_or_function)
    parameter_names = [a for a in spec.args if a != "self"]
    accept_any_args = spec.varargs is not None
    accept_any_kwargs = spec.varkw is not None

    args = []
    if accept_any_args and len(parameter_names) == 0:
        args = list(translated_args)
    else:
        for i, arg in enumerate(parameter_names):
            if i < len(translated_args):
                args.append(translated_args[i])
            elif arg in translated_kwargs:
                args.append(translated_kwargs[arg])
                del translated_kwargs[arg]
            elif arg in config:
                args.append(config[arg])
                del config[arg]
            elif i >= len(parameter_names) - len(spec.defaults or []):
                pass
            else:
                raise ValueError(f"Missing required argument: {arg}")

    kwargs = {}
    if accept_any_kwargs:
        kwargs = config

    return class_or_function(*args, **kwargs)
