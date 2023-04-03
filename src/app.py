from os.path import abspath, dirname, join

import flask
import structlog

from src import settings

log = structlog.get_logger(__name__)


class App(flask.Flask):
    def run(self, *args, **kwargs):
        # Only generate types files in development
        if settings.in_dev_environment:
            from src.apis.types_manager import write_types

            log.info(app.url_map)

            write_types()

        return super().run(*args, **kwargs)


app = App(
    __name__,
    static_folder=abspath(join(dirname(__file__), "static")),
    template_folder=abspath(join(dirname(__file__), "template")),
)

from src import views


def initialise_app(application: str) -> None:
    """
    Initalise application. Set configuration here.
    """
    if settings.in_dev_environment:
        app.jinja_env.auto_reload = True
