from os import environ

ENVIRONMENT = environ.get("ENVIRONMENT", "development")

in_dev_environment = ENVIRONMENT == "development"
