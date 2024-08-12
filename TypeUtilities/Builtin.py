from types import UnionType, NoneType


def is_builtin_type(item: type | UnionType) -> bool:
    """
    Checks if the item is a builtin type (not an inherited type of builtin type)
    :param item: The item to check
    :return: True if the item is a builtin type, False otherwise
    """
    builtin_types = [str, int, float, complex, list, tuple, range, dict, set, frozenset, bool, bytes, bytearray,
                     memoryview, NoneType]
    return item in builtin_types

