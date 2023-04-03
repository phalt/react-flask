"""
A simple example Flask Render React app
"""

import attrs

from src.apis.blueprint import Blueprint
from src.apis.types import APIResponse
from src.app import app
from src.render_react.renderer import render_html, render_react

blueprint = Blueprint("example", __name__, url_prefix="/example")


@blueprint.route("/")
@render_html()
def base_page():
    """
    This is your standard flask route and just returns a simple template file.
    """
    return dict(hello="world")


@attrs.define
class GetRouteResponse(APIResponse):
    kia: str


@blueprint.api_get_route("/get")
def get_example() -> GetRouteResponse:
    """
    This is an example API GET route.
    """
    return GetRouteResponse(kia="ora")


@attrs.define
class PostRouteResponse(APIResponse):
    result: str


@blueprint.api_post_route("/post")
def post_example(parameter_one: str) -> PostRouteResponse:
    """
    This is an example API GET route.
    """
    return PostRouteResponse(result=parameter_one)


@attrs.define
class ExamplePageProps:
    good: str


@blueprint.route("/react")
@render_react()
def react_example() -> ExamplePageProps:
    return ExamplePageProps(good="day")


app.register_blueprint(blueprint)
