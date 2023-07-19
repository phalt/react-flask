from __future__ import annotations

import typing
from os.path import exists
from pathlib import Path

import flask
import structlog

from src import settings
from src.app import app
from src.utils import unwrap

log = structlog.getLogger(__name__)


def build_render_context_for_base_template() -> typing.Dict[str, typing.Any]:
    """
    Return the render context required for base.jinja2
    """
    blueprint_id = unwrap(flask.request.blueprint).replace(".", "-")

    html_classes = [f"blueprint-{blueprint_id}"]

    return {
        "html_classes": html_classes,
        "html_id": f"endpoint-{unwrap(flask.request.endpoint).replace('.', '-')}",
        "is_development": settings.in_dev_environment,
    }


def write_react_page_file(module: str, endpoint: str) -> None:
    """
    Create a simple template file for a React page component if one does not exist yet.
    Will only run if ENVIRONMENT is set to development
    """
    if not settings.in_dev_environment:
        return
    react_page_file_path = (
        Path(app.root_path) / "js" / "template" / module / f"{endpoint}.tsx"
    )
    template_path = Path(app.root_path) / "template" / "beckett_page.template"

    if not exists(react_page_file_path):
        log.info(
            "Creating new beckett page for this endpoint",
            module=module,
            endpoint=endpoint,
            filename=str(react_page_file_path),
        )
        with template_path.resolve().open("r") as template_file:
            template_file_content = template_file.read()
            template_file_content = template_file_content.replace(
                "{{endpoint}}", endpoint
            )
        react_page_file_path.parent.mkdir(exist_ok=True)
        with react_page_file_path.resolve().open("w+") as new_file:
            new_file.write(template_file_content)
    return


def write_typescript_file(
    *,
    module: str,
    endpoint: str,
    type_data: typing.Optional[str],
) -> None:
    """Intelligently writes typing data to the named file.

    Ensures the directory the file is meant to be in is created, if it doesn't exist already, and removes the directory
    the file was meant to be in if the file has been removed because the type data is gone.

    Only writes the file if the type data has changed to prevent excessive writes.

    Doesn't attempt to write the files unless the server is running in development mode.
    """
    if settings.ENVIRONMENT != "development":
        return

    typescript_file_path = (
        Path(app.root_path) / "js" / "template" / module / f"{endpoint}.type.ts"
    ).resolve()
    try:
        with typescript_file_path.open() as fh:
            existing_type_data = fh.read()
    except IOError:
        existing_type_data = None

    if type_data != existing_type_data:
        if type_data:
            log.info(
                "writing new type data",
                module=module,
                endpoint=endpoint,
                filename=str(typescript_file_path),
            )

            # Create the directory if it's not already there.
            typescript_file_path.parent.mkdir(exist_ok=True)

            with typescript_file_path.open("w") as fh:
                fh.write(type_data)
        else:
            log.info(
                "removing type data",
                module=module,
                endpoint=endpoint,
                filename=str(typescript_file_path),
            )

            typescript_file_path.unlink()

            # Remove the directory if empty. The pythonic way might be to try it and catch the exception, but in this
            # case we'd rather not even try if we have even an inkling that there might still be a file in there.
            if any(typescript_file_path.parent.iterdir()):
                typescript_file_path.parent.rmdir()
