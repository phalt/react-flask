import flask
import structlog

from src import settings

log = structlog.get_logger(__name__)


class BeckettApp(flask.Flask):
    def __init__(self, *args, **kwargs):
        assert (
            "static_folder" in kwargs.keys()
        ), "static_folder must be set for Beckett to work with Flask"
        assert (
            "template_folder" in kwargs.keys()
        ), "template_folder must be set for Beckett to work with Flask"
        super().__init__(*args, **kwargs)

    def run(self, *args, **kwargs):
        # Only generate TS types files in development
        if settings.in_dev_environment:
            from src.beckett.types.types_manager import api_route_type_manager

            api_route_type_manager.write_types()

            log.info(f"URLs: {self.url_map}")

        extra_files = [settings.BECKETT_METAFILE_PATH]

        return super().run(*args, **kwargs, extra_files=extra_files)
