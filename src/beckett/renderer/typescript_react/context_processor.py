import json

import flask

from src.settings import BECKETT_METAFILE_PATH


def register_react_helper():
    metafile_path = BECKETT_METAFILE_PATH
    try:
        with open(metafile_path, "r") as fh:
            metafile = json.loads(fh.read())
    except FileNotFoundError as e:
        raise Exception("`metafile.json` is missing. Have you run 'make web'?") from e

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
