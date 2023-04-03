import structlog

log = structlog.get_logger(__name__)


def write_types():
    log.info("Generating API Types...")
