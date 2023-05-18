import click


@click.group(invoke_without_command=False)
def app():
    """Run server"""


@app.command(name="run")
def run():
    from src import settings
    from src.app import app

    app.run(
        debug=settings.in_dev_environment,
        port=9000,
        host="0.0.0.0",
    )
