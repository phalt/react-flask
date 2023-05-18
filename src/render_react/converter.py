from decimal import Decimal
from enum import Enum
from typing import (
    Any,
    Literal,
    Optional,
    Type,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)
from uuid import UUID

from cattr import GenConverter
from cattr.preconf.json import make_converter

from src.apis.types import NoneType


def _base_converter() -> GenConverter:
    """
    Create a cattr converter designed for structuring/unstructuring data the way that React requires it for Admin.

    For both requests (structring) and responses (unstructuring), we're rendering from/to JSON, which means the
    converters can assume that simple types like `str` and `int` are available.
    """
    converter = make_converter(forbid_extra_keys=True)

    converter.register_unstructure_hook(UUID, lambda u: str(u) if u else None)  # type: ignore
    converter.register_structure_hook(UUID, lambda u, _: UUID(u) if u else None)

    def convert_to_decimal_type(data: Any) -> Optional[Decimal]:
        if type(data) is Decimal:
            return data
        if type(data) is str:
            return None if len(data) == 0 else Decimal(data)
        if type(data) is int:
            return Decimal(data)
        if type(data) is NoneType:
            return None
        if type(data) is dict:
            return Decimal(data["$decimal"])
        else:
            raise NotImplementedError(
                f"_convert_to_decimal_type: Unsupported type '{type(data)}'"
            )

    converter.register_unstructure_hook(Decimal, lambda d: str(d))  # type: ignore
    converter.register_structure_hook(Decimal, lambda d, _: convert_to_decimal_type(d))

    def try_get_type_literal(input_type: Type) -> Optional[str]:
        try:
            type_literal = get_type_hints(input_type)["type"]
            assert get_origin(type_literal) is Literal
            values = get_args(type_literal)
            assert (
                len(values) == 1
            )  # It's possible to declare a literal with multiple values. We can't handle those.
            return get_args(type_literal)[0]
        except Exception:
            return None

    def is_union_with_type_literals(input_type: Type) -> bool:
        if get_origin(input_type) != Union:
            return False
        unioned_types = get_args(input_type)
        return all([try_get_type_literal(t) is not None for t in unioned_types])

    def structure_union(input: Any, input_type: Type) -> str:
        type_map = dict()
        for t in get_args(input_type):
            type_literal = try_get_type_literal(t)
            assert (
                type_literal
            ), "Expected all unioned types to have a literal 'type' member"
            type_map[type_literal] = t
        return type_map[input["type"]](**input)

    converter.register_structure_hook_func(is_union_with_type_literals, structure_union)

    # Cattrs will coerce some types by default. Override this to instead pass these types straight through
    def strict_passthrough(val: Any, cls: Type[Any]) -> Any:
        if val is None:
            return None

        return val

    converter.register_structure_hook(str, strict_passthrough)
    converter.register_structure_hook(int, strict_passthrough)

    return converter


def _create_get_converter() -> GenConverter:
    """
    Create a cattr converter designed for structuring data sourced from a GET request.

    In a GET request, all data arrives via the URL as strings, as opposed to a POST where JSON means data can arrive as
    primitive types (ints, for example). Converters created by this function are more tolerant of certain types arriving
    as string.
    """

    # Because get requests are entirely strings, we need to be a bit more lenient here
    converter = _base_converter()

    # The default cattrs enum structure hook will freak out when passed ''
    # For get requests, this should return None
    def convert_to_enum_type(data: Any, type_: Type[Enum]) -> Optional[Enum]:
        if not data:  # If it's falsey - matching '' or None
            return None

        try:
            return type_(data)
        except ValueError:
            raise Exception(f"{data} not in literal {type_}") from None

    converter.register_structure_hook(
        Enum, convert_to_enum_type
    )  # type:ignore  # Mypy's generic support is... not great

    # Get parameters will always pass ints as string, so we need to do a bit of coercion here
    converter.register_structure_hook(int, lambda v, _: None if v is None else int(v))

    return converter


converter = _base_converter()

get_request_converter = _create_get_converter()
