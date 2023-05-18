import json
import pathlib
from os.path import abspath, dirname, join

import flask
import structlog

from src import settings

log = structlog.get_logger(__name__)


class App(flask.Flask):
    def run(self, *args, **kwargs):
        # Only generate TS types files in development
        if settings.in_dev_environment:
            from src.apis.types_manager import api_route_type_manager

            log.info(f"\nURL map: \n {app.url_map}")

            api_route_type_manager.write_types()

        return super().run(*args, **kwargs)


app = App(
    __name__,
    static_folder=abspath(join(dirname(__file__), "static")),
    template_folder=abspath(join(dirname(__file__), "template")),
)

from src import views  # noqa


def initialise_app(application: str) -> None:
    """
    Initalise application. Set configuration here.
    """
    if settings.in_dev_environment:
        app.jinja_env.auto_reload = True


# The unexpected ../../ is because Path treats __init__.py as a directory
metafile_path = pathlib.Path(__file__) / ".." / ".." / "metafile.json"
try:
    with open(metafile_path.resolve(), "r") as fh:
        metafile = json.loads(fh.read())
except FileNotFoundError as e:
    raise Exception("`metafile.json` is missing. Have you run 'make web'?") from e


@app.context_processor
def register_js_helpers():
    def es_module(name: str) -> str:
        """
        Returns the built static file path for a given original TS file

        es_module("js/Example.tsx") -> "/static/Example-ABD123.js"
        """
        if name not in metafile:
            raise KeyError(
                f"'{name}' isn't defined in the metafile and hasn't been built. Do you need to run 'make web'?"
            )

        return flask.url_for("static", filename=metafile[name])

    return dict(es_module=es_module)
