import enum
import typing
from decimal import Decimal
from typing import Any, Literal, Tuple, Union, get_args, get_origin
from uuid import UUID

from pydantic import BaseModel
from pydantic.fields import FieldInfo

from src.beckett.renderer.typescript_react.imports import TypescriptImports
from src.beckett.renderer.typescript_react.interfaces import TypescriptInterfaces

NoneType = type(None)


def generate_type(
    type_: Any,
    imports: TypescriptImports,
) -> str:
    if type_ is int:
        return "number"
    if type_ is str:
        return "string"
    if type_ is bool:
        return "boolean"
    if type_ is float:
        return "number"
    if type_ is dict:
        return "Record<string, any>"
    if type_ is Decimal:
        return "string"
    if type_ is NoneType:
        return "undefined"
    if type_ is UUID:
        return "string"
    if isinstance(type_, enum.EnumMeta):
        return " | ".join(f'"{v.value}"' for v in type_)  # type: ignore

    origin = get_origin(type_)
    args = get_args(type_)

    if origin is Union:
        return " | ".join(generate_type(a, imports) for a in args)
    if origin is dict:
        if len(args) == 0:
            return "Record<string, any>"
        return f"Record<{generate_type(args[0], imports)}, {generate_type(args[1], imports)}>"
    if origin is tuple:
        return "[" + ", ".join(generate_type(a, imports) for a in args) + "]"
    if origin is list:
        return "".join(generate_type(a, imports) for a in args) + "[]"
    if origin is Literal:
        return f'"{args[0]}"'

    raise TypeError(f"Can't generate interface for {type_} (type={type(type_)})")


def generate_interfaces(
    cls: Any,
    name: typing.Optional[str] = None,
    default_export: typing.Optional[bool] = False,
) -> Tuple[TypescriptImports, TypescriptInterfaces]:
    if name is None:
        name = cls.__name__

    imports = TypescriptImports()
    interfaces = TypescriptInterfaces()

    # Generate interface for the class we've been passed.
    if default_export:
        declaration = "default interface " + name + " {\n"
    else:
        declaration = "interface " + name + " {\n"

    for field_name, field_info in cls.model_fields.items():
        # check to see if it is wrapped in a typing.Optional[]
        inner_type, was_optional = strip_optional_type_wrapper(field_info)

        # check to see if it is wrapped in a typing.List[]
        inner_type, was_list = strip_list_type_wrapper(inner_type)

        if (union_types := strip_union_type_wrapper(inner_type)) is not None:
            # make sure all the unioned types have declarations of their own
            type_names = []
            for union_type in union_types:
                child_imports, child_interfaces = generate_interfaces(union_type)

                imports.merge(child_imports)
                interfaces.merge(child_interfaces)

                type_names.append(union_type.__name__)
            # The class we've been passed can declare its use of the union now
            declaration += f'    "{field_name}": ({("| ".join(type_names))})'

        # check to see if it is a custom defined type
        elif hasattr(inner_type, "__pydantic_complete__"):
            # We've found an object that needs interface(s) of its own.
            child_imports, child_interfaces = generate_interfaces(inner_type)

            imports.merge(child_imports)
            interfaces.merge(child_interfaces)

            # The class we've been passed can declare its use of the object.
            declaration += f"    {field_name}: {inner_type.__name__}"
        else:
            # Simple type (not an object), just declare we use it.
            declaration += f'    "{field_name}": {generate_type(inner_type, imports)}'

        declaration += "[]" if was_list else ""
        declaration += " | undefined" if was_optional else ""
        declaration += "\n"

    declaration += "}"

    interfaces.add(name, declaration)

    return imports, interfaces


def strip_optional_type_wrapper(
    field_info: FieldInfo,
) -> typing.Tuple[type | None, bool]:
    """Given a type, get rid of the typing.Optional wrapping it, if there is one."""
    origin = typing.get_origin(field_info.annotation)
    args = typing.get_args(field_info.annotation)

    if origin is Union and len(args) == 2 and NoneType in args:
        inner_type = next(a for a in args if a is not NoneType)
        return inner_type, True
    else:
        return field_info.annotation, False


def strip_list_type_wrapper(type_hint: Any) -> typing.Tuple[type, bool]:
    """Given a type, get rid of the typing.List wrapping it, if there is one."""
    origin = typing.get_origin(type_hint)
    args = typing.get_args(type_hint)

    if origin is list:
        inner_type = args[0]
        return inner_type, True
    else:
        return type_hint, False


def strip_union_type_wrapper(type_hint: Any) -> typing.Optional[typing.List[type]]:
    origin = typing.get_origin(type_hint)
    args = typing.get_args(type_hint)
    if origin is Union and (len(args) > 2 or NoneType not in args):
        return list(args)

    return None


class PageProps(BaseModel):
    """The return class for any React Page"""


class APIResponse(BaseModel):
    """The base class for any value returned from a @beckett.api_get- or a @beckett.api_post endpoints."""  # noqa

    status_code: int = 200
    """The HTTP status code that this response will send."""


class BadRequest(APIResponse):
    status_code: int = 400
    message: str


class Forbidden(APIResponse):
    status_code: int = 403


class NotFound(APIResponse):
    status_code: int = 404


class InternalServerError(APIResponse):
    status_code: int = 500


class PydanticValidationResponse(APIResponse):
    status_code: int = 500
    message: typing.List[str]
