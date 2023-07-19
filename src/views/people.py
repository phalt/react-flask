"""
A simple example Beckett app
"""


from pydantic import BaseModel

from src.app import app
from src.beckett.blueprint import BeckettBlueprint
from src.beckett.types import APIResponse, PageProps

beckett = BeckettBlueprint("people", __name__, url_prefix="/people")


class Details(BaseModel):
    test: str


class GetPeopleResponse(APIResponse):
    name: str = "pauldefault"


@beckett.api_get("/get")
def get_people() -> GetPeopleResponse:
    """
    This is an example API GET route.
    """
    return GetPeopleResponse(name="Paul")


class PostRouteResponse(APIResponse):
    result: str


@beckett.api_post("/post")
def post_example(parameter_one: str) -> PostRouteResponse:
    """
    This is an example API GET route.
    """
    return PostRouteResponse(result=parameter_one)


class ExamplePageProps(PageProps):
    good: str


@beckett.route("/")
@beckett.page()
def react_example() -> ExamplePageProps:
    return ExamplePageProps(good="day")


@beckett.route("/test/<name>")
@beckett.page()
def test_page(name: str) -> ExamplePageProps:
    return ExamplePageProps(good=name)


app.register_blueprint(beckett)
