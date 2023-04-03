import click


@click.group(invoke_without_command=False)
def app():
    """Run server"""


@app.command(name="run")
def run():
    from src import settings
    from src.app import app, initialise_app

    initialise_app("Example server")
    # The metafile.json changes every time a JS file changes, we want to reload whenever that happens
    # because the JS output will change!
    extra_files = ["metafile.json"]
    app.run(
        debug=settings.in_dev_environment,
        port=9000,
        host="0.0.0.0",
        extra_files=extra_files,
    )
