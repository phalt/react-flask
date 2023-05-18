"""
A simple example Flask Render React app
"""

import attrs

from src.app import app
from src.beckett.blueprint import BeckettBlueprint
from src.beckett.renderer.html.renderer import render_html
from src.beckett.renderer.typescript_react.renderer import beckett_page
from src.beckett.types import APIResponse

blueprint = BeckettBlueprint("example", __name__, url_prefix="/example")


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


@blueprint.api_get("/get")
def get_example() -> GetRouteResponse:
    """
    This is an example API GET route.
    """
    return GetRouteResponse(kia="ora")


@attrs.define
class PostRouteResponse(APIResponse):
    result: str


@blueprint.api_post("/post")
def post_example(parameter_one: str) -> PostRouteResponse:
    """
    This is an example API GET route.
    """
    return PostRouteResponse(result=parameter_one)


@attrs.define
class ExamplePageProps:
    good: str


@blueprint.route("/react")
@beckett_page()
def react_example() -> ExamplePageProps:
    return ExamplePageProps(good="day")


app.register_blueprint(blueprint)
