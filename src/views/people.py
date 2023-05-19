"""
A simple example Flask Render React app
"""

import attrs

from src.app import app
from src.beckett.blueprint import BeckettBlueprint
from src.beckett.renderer.typescript_react.renderer import beckett_page
from src.beckett.types import APIResponse

blueprint = BeckettBlueprint("people", __name__, url_prefix="/people")


@attrs.define
class GetPeopleResponse(APIResponse):
    name: str


@blueprint.api_get("/get")
def get_people() -> GetPeopleResponse:
    """
    This is an example API GET route.
    """
    return GetPeopleResponse(name="Paul")


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


@blueprint.route("/")
@beckett_page()
def react_example() -> ExamplePageProps:
    return ExamplePageProps(good="day")


app.register_blueprint(blueprint)
