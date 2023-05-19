"""
Index.py - provides a simple html example
"""
from src.app import app
from src.beckett.blueprint import BeckettBlueprint
from src.beckett.renderer.html.renderer import render_html

blueprint = BeckettBlueprint("index", __name__, url_prefix="/")


@blueprint.route("/")
@render_html()
def base_page():
    """
    This is your standard flask route and just returns a simple template file.
    Beckett doesn't just auto generate React frontend pages, it also does Jinja2 pages, too!
    """
    return dict(hello="world")


app.register_blueprint(blueprint)
