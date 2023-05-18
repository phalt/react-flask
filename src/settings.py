from os import environ
from os.path import abspath, dirname, join

ENVIRONMENT = environ.get("ENVIRONMENT", "development")

in_dev_environment = ENVIRONMENT == "development"

BECKETT_METAFILE_PATH = abspath(join(dirname(__file__), "metafile.json"))
