import flask
import structlog

from src.apis.types_manager import generate_api_decorator

log = structlog.get_logger(__name__)


class Blueprint(flask.Blueprint):
    """
    Handles API URL registration
    """

    def api_get_route(self, rule, *, endpoint=None, **options):
        if "methods" in options:
            raise Exception("Can't specify method for api_get_route")

        def decorator(f):
            actual_endpoint = endpoint or f.__name__
            handle_api_route = generate_api_decorator(
                f,
                method="GET",
                endpoint=f"{self.name}.{actual_endpoint}",
                url=self.url_prefix + rule,
            )

            return self.add_url_rule(
                rule,
                view_func=handle_api_route,
                methods=["GET"],
                endpoint=actual_endpoint,
                **options,
            )

        return decorator

    def api_post_route(self, rule, *, endpoint=None, **options):
        if "methods" in options:
            raise Exception("Can't specify method for api_post_route")

        def decorator(f):
            actual_endpoint = endpoint or f.__name__
            handle_api_route = generate_api_decorator(
                f,
                method="POST",
                endpoint=f"{self.name}.{actual_endpoint}",
                url=self.url_prefix + rule,
            )

            return self.add_url_rule(
                rule,
                view_func=handle_api_route,
                methods=["POST"],
                endpoint=actual_endpoint,
                **options,
            )

        return decorator
