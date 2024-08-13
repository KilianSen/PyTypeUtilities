from types import UnionType, GenericAlias
from typing import Literal, List, Union

from TypeUtilities.Builtin import is_builtin_type

# TODO: Add capability to traverse/resolve optional types

def is_union_type(item: type | UnionType) -> bool:
    """
    Checks if the item is a Union type (not an inherited type of Union)
    :param item: The item to check
    :return: True if the item is a Union type, False otherwise
    """
    return type(item) is UnionType and hasattr(item, '__args__')

def strip_union_types(item: UnionType, stripped: List[type] | type | UnionType) -> type | UnionType:
    """
    Strips the Union types from the item
    :param item: The input type to strip from
    :param stripped: The types to strip from the item
    :return: The stripped type or Union type (if multiple types are left)
    """
    if not is_union_type(item):
        if type(item) is type or isinstance(item, GenericAlias): # FIXME: Workaround for Lists might not be robust enough
            return item
        raise ValueError(f'Invalid type {item}')

    if type(stripped) not in [list, type, UnionType]:
        raise Exception(f'Invalid strip type {stripped}')

    filters = []
    if type(stripped) is list:
        filters = stripped
    elif type(stripped) is type:
        filters = [stripped]
    elif type(stripped) is UnionType:
        filters = [t for t in stripped.__args__]

    output = []
    for t in item.__args__:
        if t not in filters:
            output.append(t)

    if len(output) == 1:
        return output[0]

    return Union[tuple(output)]


def resolve_union_to_builtin_type(item: UnionType | type, extension: List[type] | UnionType = None,
                                  search_mode: Literal["inorder depth first" , "count"] = "inorder depth first") -> type:
    """
    Resolves a Union type to a builtin type
    :param item:
    :param extension: Additional types to consider as resolved types
    :param search_mode: "inorder depth first": Traverses the Union type in order and returns the first builtin type.
    "count": Returns the most common builtin type in the Union type
    :return:
    """

    # check if item is already a builtin type
    if is_builtin_type(item) or item in extension:
        return item

    # check if item is a UnionType
    if not is_union_type(item):
        raise ValueError(f'Invalid type {item}')

    # check if item is a UnionType with only one type
    if len(item.__args__) == 1:
        return item.__args__[0]

    if search_mode == "inorder depth first":
        for t in item.__args__:
            return resolve_union_to_builtin_type(t, extension, search_mode)

        raise ValueError(f'No builtin type found in {item}')
    elif search_mode == "count":
        flat = flatten_union_types(item, recursive=True, multiple=True)
        counts = {}
        for t in flat:
            if t not in counts:
                counts[t] = 0
            counts[t] += 1

        sorted_types = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        for t, c in sorted_types:
            if is_builtin_type(t) or t in extension:
                return t
        raise ValueError(f'No builtin type found in {item}')

    raise ValueError(f'Invalid search mode {search_mode}')

def flatten_union_types(item: UnionType, recursive: bool = False, multiple: bool = False) -> List[type]:
    """
    Flattens a Union type (tree structure) to a list
    :param item: The Union type to flatten
    :param recursive: If True, flattens the Union type recursively
    :param multiple: If True, returns a list of all types in the Union type. If False, returns a list of unique types
    :return: A list of types
    """
    if not is_union_type(item):
        raise ValueError(f'Invalid type {item}')

    if not recursive:
        return [x for x in item.__args__]

    output = []
    for t in item.__args__:
        if is_union_type(t):
            output.extend(flatten_union_types(t, recursive))
        else:
            output.append(t)

    return output if multiple else list(set(output))
