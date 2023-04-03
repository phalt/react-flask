from __future__ import annotations

import enum
import typing
from functools import wraps
from pathlib import Path

import flask
import structlog

from src import settings
from src.apis.types import NoneType, generate_interfaces
from src.render_react.converter import converter
from src.utils import unwrap

log = structlog.getLogger(__name__)


def _build_render_context_for_base_template() -> typing.Dict[str, typing.Any]:
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


class render_html:
    def __init__(
        self,
        template=None,
    ):
        self.template = template

    def __call__(self, f, template=None):
        @wraps(f)
        def wrapped(*args, **kwargs):
            response = f(*args, **kwargs)

            if not isinstance(response, dict):
                return response

            template = self.template

            if template is None:
                directory = "/".join(f.__module__.split(".")[2:])
                template = f"/{directory}/{f.__name__}.jinja2"

            log.info(f"Looking for {template}...")

            out = flask.render_template(
                template,
                **response,
                **_build_render_context_for_base_template(),
                **getattr(flask.g, "context", {}),
            )

            status = 200
            headers = {
                "Content-Type": "text/html; charset=utf-8",
            }

            return out, status, headers

        return wrapped
