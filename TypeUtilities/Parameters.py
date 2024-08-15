from typing import Tuple, List


def get_default_parameters(func) -> List[Tuple[str, type, any]]:
    annots = list(func.__annotations__.items().__reversed__())
    fields = [x[0] for x in annots]
    types = [x[1] for x in annots]
    defaults = func.__defaults__[::-1]

    return list(x for x in zip(fields, types, defaults))[::-1]

def get_parameters(func) -> List[Tuple[str, type]]:
    return list(x for x in func.__annotations__.items() if x[0] != 'return')

def get_return_type(func) -> type:
    return func.__annotations__['return'] if 'return' in func.__annotations__ else None

