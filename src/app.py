from os.path import abspath, dirname, join

from src.beckett.app import BeckettApp
from src.beckett.renderer.typescript_react.context_processor import (
    register_react_helper,
)

app = BeckettApp(
    __name__,
    static_folder=abspath(join(dirname(__file__), "static")),
    template_folder=abspath(join(dirname(__file__), "template")),
)

from src import views  # noqa

app.context_processor(register_react_helper)
