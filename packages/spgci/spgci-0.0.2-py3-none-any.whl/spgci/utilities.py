from typing import List, Union, Any, TypeVar, Collection, Optional
from pandas import Series
from typing_extensions import TypeGuard
from enum import Enum

T = TypeVar("T", bound=Enum)


def list_to_filter(
    field_name: str,
    items: Optional[
        Union[
            Collection[str],
            Collection[int],
            Collection[T],
            str,
            int,
            T,
        ]
    ] = None,
) -> str:
    if isinstance(items, Series):
        return convert_series_to_filterexp(field_name, items)

    if not items:
        return ""

    if isinstance(items, str):
        return f'{field_name}: "{items}"'
    if isinstance(items, Enum):
        return f'{field_name}: "{items.value}"'
    if isinstance(items, int):
        return f"{field_name}: {items}"

    if is_enum_list(items):
        n_items: List[str] = [x.value for x in items]
        n_items = ['"' + x + '"' for x in n_items]
    elif is_str_list(items):
        n_items = ['"' + x + '"' for x in items]
    elif is_int_list(items):
        n_items = [str(x) for x in items]
    else:
        raise TypeError("not supported")

    return f"{field_name} IN ({','.join(n_items)})"


def convert_series_to_filterexp(field_name: str, s: "Series[Any]") -> str:
    # print(s.d)
    if is_int_list(s):
        l = [str(x) for x in s]
    elif is_str_list(s):
        l = ['"' + x + '"' for x in s]
    else:
        raise TypeError("not supported")

    return f"{field_name} IN ({','.join(l)})"


def is_enum_list(lst: Collection[Any]) -> TypeGuard[List[Enum]]:
    return all(isinstance(x, Enum) for x in lst)


def is_str_list(lst: Collection[Any]) -> TypeGuard[List[str]]:
    return all(isinstance(x, str) for x in lst)


def is_int_list(lst: Collection[Any]) -> TypeGuard[List[int]]:
    return all(isinstance(x, int) for x in lst)
