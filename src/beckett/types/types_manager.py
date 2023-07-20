import json
import os
import re
import typing
from dataclasses import dataclass
from types import CodeType
from typing import Any, Callable, Dict, List, Literal, Set, Tuple, Type, Union

import flask
import structlog
import werkzeug
from pydantic import BaseModel, ValidationError, create_model

from src.beckett.renderer.typescript_react.imports import TypescriptImports
from src.beckett.renderer.typescript_react.interfaces import TypescriptInterfaces
from src.utils import unwrap

from .types import (
    APIResponse,
    BadRequest,
    Forbidden,
    InternalServerError,
    NotFound,
    PydanticValidationResponse,
    generate_interfaces,
)

log = structlog.get_logger(__name__)


def _stringify_code_location(code: CodeType) -> str:
    """
    Takes a CodeType object and produces a string location of that code.

    This is used for comments in the generated types to help developers find the source code for a given type
    """

    from src.app import app

    return os.path.relpath(code.co_filename, os.path.join(app.root_path, "..", ".."))


@dataclass
class RouteDefinition:
    method: str
    request: BaseModel
    responses: typing.List[Union[Type[APIResponse], Type[None]]]
    endpoint: str
    code: CodeType
    url: str


class APIRouteTypeManager:
    """
    This class collects all the `api_get_route` and `api_post_route` calls from the `auth_blueprint`, extracts
    type information from them and writes out `js/api/types.ts`
    """

    _names: Set[str]
    _routes: Dict[str, RouteDefinition]

    def __init__(self):
        self._names = set()
        self._routes = dict()

    @classmethod
    def get_types_path(cls) -> str:
        from src.app import app

        return os.path.abspath(os.path.join(app.root_path, "js", "api", "types.ts"))

    def _get_unique_name(self, name: str) -> str:
        name = name[0].upper() + name[1:]
        name = re.sub(r"[^A-Za-z]+(\w)", lambda match: match[1].upper(), name)
        if name in self._names:
            i = 1
            while f"{name}{i}" in self._names:
                i += 1
            name = f"{name}{i}"
        self._names.add(name)
        return name

    def add_route(
        self,
        *,
        method: Literal["GET", "POST"],
        request: Any,
        responses: List[Union[Type[APIResponse], Type[None]]],
        endpoint: str,
        url: str,
        code: CodeType,
    ) -> None:
        if endpoint in self._routes:
            raise ValueError(f"API endpoint already exists: {endpoint}")

        self._routes[endpoint] = RouteDefinition(
            method=method,
            request=request,
            responses=responses,
            endpoint=endpoint,
            code=code,
            url=url,
        )

    def get_url_map(self) -> Dict[str, str]:
        return {
            endpoint: definition.url for endpoint, definition in self._routes.items()
        }

    def write_types(self) -> None:
        log.info("Generating types...")
        with open(self.get_types_path(), "w") as fh:
            fh.write(self.generate_types())

    def generate_types(self) -> str:
        import inspect

        out = (
            f"""
/*
THIS FILE IS AUTO-GENERATED, DO NOT ALTER MANUALLY.

Please see {_stringify_code_location(unwrap(inspect.currentframe()).f_code)}
*/
        """.strip()
            + "\n"
        )

        typescript_imports = TypescriptImports()
        typescript_interfaces = TypescriptInterfaces()

        endpoint_names: Dict[str, Tuple[str, List[str]]] = {}

        for endpoint, definition in sorted(self._routes.items()):
            endpoint_name = self._get_unique_name(endpoint)
            endpoint_names[endpoint] = (endpoint_name, [])
            if len(definition.request.model_fields.items()) > 0:
                # Only output types if function has args
                request_imports, request_interfaces = generate_interfaces(
                    definition.request, name=endpoint_name + "Request"
                )
                typescript_imports.merge(request_imports)
                typescript_interfaces.merge(request_interfaces)

            for response in definition.responses:
                if isinstance(None, response):
                    continue

                response_type_name = self._get_unique_name(endpoint_name + "Response")
                endpoint_names[endpoint][1].append(response_type_name)

                response_imports, response_interfaces = generate_interfaces(
                    response, name=response_type_name
                )

                typescript_imports.merge(response_imports)
                typescript_interfaces.merge(response_interfaces)

        out += typescript_imports.render()
        out += "\n"
        out += typescript_interfaces.render()

        def write_endpoint(d: RouteDefinition, undefined: str = "undefined") -> str:
            endpoint_name, response_names = endpoint_names[d.endpoint]
            response_union = (
                " | ".join(name for name in response_names)
                if response_names
                else "undefined"
            )

            # Mark as optional if there's a non-optional type and an optional type
            response_optionality = (
                "?"
                if response_names
                and any(isinstance(None, resp) for resp in d.responses)
                else ""
            )

            request_type = (
                endpoint_name + "Request"
                if len(d.request.model_fields.items()) > 0
                else undefined
            )
            return (
                f"    // {_stringify_code_location(d.code)}\n"
                "    "
                + json.dumps(endpoint)
                + ": {request: "
                + request_type
                + ", response"
                + response_optionality
                + ": "
                + response_union
                + "}\n"
            )

        out += "// prettier-ignore\n"
        out += "export interface GET_MAP {\n"
        for endpoint, definition in sorted(self._routes.items()):
            if definition.method != "GET":
                continue
            out += write_endpoint(definition)

        out += "}\n\n"

        out += "// prettier-ignore\n"
        out += "export interface POST_MAP {\n"
        for endpoint, definition in sorted(self._routes.items()):
            if definition.method != "POST":
                continue
            out += write_endpoint(definition, undefined="{}")

        out += "}\n"
        return out


api_route_type_manager = APIRouteTypeManager()


def _strip_optional_type_wrapper(type_hint: Any) -> Tuple[type, bool]:
    """Given a type, get rid of the typing.Optional wrapping it, if there is one."""
    origin = typing.get_origin(type_hint)
    args = typing.get_args(type_hint)

    if origin is Union and len(args) == 2 and type(None) in args:
        inner_type = next(a for a in args if a is not type(None))
        return inner_type, True
    else:
        return type_hint, False


def _make_field(raw_type: type):
    _, is_optional = _strip_optional_type_wrapper(raw_type)

    return (
        raw_type,
        # ... will set this field to required
        None if is_optional else ...,
    )


def generate_request_response_classes(
    func: Callable,
) -> Tuple[type[BaseModel], typing.List[Union[Type[APIResponse], Type[None]]]]:
    request_hints = typing.get_type_hints(func)

    # Response can either be None, Type, or Union[Type, Type...]
    return_type = request_hints.pop("return", None)

    if typing.get_origin(return_type) == typing.Union:
        response_types = list(typing.get_args(return_type))
    else:
        response_types = [return_type]

    for single_type in response_types:
        assert isinstance(None, single_type) or issubclass(
            single_type, APIResponse
        ), "Function must return APIResponse or None"

    # Build request class based on parameter names
    Request = create_model(
        "Request", **{k: _make_field(v) for k, v in request_hints.items()}
    )

    return Request, response_types


def api_response_as_flask_response(response: APIResponse) -> flask.Response:
    """Converts an APIResponse into a flask Response."""
    flask_response = flask.Response(
        response.model_dump_json(), mimetype="application/json"
    )
    flask_response.status_code = response.status_code

    return flask_response


def generate_api_decorator(
    func: Callable, *, method: Literal["GET", "POST"], endpoint: str, url: str
) -> Callable:
    Request, responses = generate_request_response_classes(func)

    api_route_type_manager.add_route(
        method=method,
        request=Request,
        responses=responses,
        endpoint=endpoint,
        code=func.__code__,
        url=url,
    )

    def handle_api_route(**kwargs):
        try:
            # Hand the request data to the class. This will validate and convert the data to the correct types.
            if method == "GET":
                request = Request(**kwargs, **flask.request.args)
            elif method == "POST":
                request = Request(**kwargs, **flask.request.json or {})
            else:
                raise TypeError(f"Invalid method: {method}")
        except Exception as e:
            error_msg = "Request payload failed validation"
            log.exception(error_msg, module=func.__module__, endpoint=endpoint, error=e)

            return api_response_as_flask_response(BadRequest(message=repr(e)))

        # Call the view function, and deal with any errors that result.
        try:
            response = func(**request.model_dump())
            if not any(isinstance(response, resp) for resp in responses):
                raise Exception("Invalid response generated by server")
        except ValidationError as e:
            log.exception(e, exc_info=e)
            return api_response_as_flask_response(
                PydanticValidationResponse(message=[str(e.errors())])
            )
        except (
            werkzeug.exceptions.Forbidden,
            werkzeug.exceptions.NotFound,
            werkzeug.exceptions.BadRequest,
        ) as e:
            # For these HTTP exceptions, we send a custom response. As these are expected, there's no need to
            # log the exceptions themselves (i.e. it's pretty standard to have a handler throw a 404).
            http_exception_to_response_lookup = {
                400: BadRequest,
                403: Forbidden,
                404: NotFound,
            }

            if e.code in http_exception_to_response_lookup:
                return api_response_as_flask_response(
                    http_exception_to_response_lookup[e.code]()
                )

            raise NotImplementedError(
                f"_http_exception_to_response doesn't know how to convert exception {e.code}: "
                f"{e.name} to a response"
            )
        except werkzeug.exceptions.HTTPException as e:
            log.exception(e, exc_info=e)

            response = flask.Response(e.get_description())
            response.status_code = e.code

            return response
        except Exception as e:
            # Everything other exception is unexpected.

            # For our logs.
            log.exception(e, exc_info=e)

            return api_response_as_flask_response(InternalServerError())

        return api_response_as_flask_response(response)

    return handle_api_route
