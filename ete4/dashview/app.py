from dash import Dash, dcc, html

from .callbacks.control_panel import register_control_panel_callbacks
from .callbacks.downloads import register_download_callbacks
from .callbacks.hover import register_hover_callbacks
from .components.control_panel import CONTROL_PANEL_STYLE, make_control_panel
from .components.tree_graph import make_tree_graph
from .draw import tree_to_plotly


BASE_STYLE = """
            html, body, #react-entry-point {
                width: 100%;
                height: 100%;
                margin: 0;
            }
"""


def make_index_string():
    return f"""<!DOCTYPE html>
<html>
    <head>
        {{%metas%}}
        <title>{{%title%}}</title>
        {{%favicon%}}
        {{%css%}}
        <style>
{BASE_STYLE}{CONTROL_PANEL_STYLE}
        </style>
    </head>
    <body>
        {{%app_entry%}}
        <footer>
            {{%config%}}
            {{%scripts%}}
            {{%renderer%}}
        </footer>
    </body>
</html>"""


def make_app_layout(fig, tree_name="current tree"):
    return html.Div(
        [
            make_tree_graph(fig),
            dcc.Download(id="download-newick"),
            dcc.Store(id="download-svg-trigger"),
            dcc.Store(id="download-image-trigger"),
            make_control_panel(tree_name),
        ],
        style={"position": "fixed", "inset": 0},
    )


def run_dash_app(tree, port=8050, tree_name="current tree"):
    fig = tree_to_plotly(tree)

    app = Dash(__name__)
    app.index_string = make_index_string()
    app.layout = make_app_layout(fig, tree_name)

    register_control_panel_callbacks(app)
    register_download_callbacks(app, tree)
    register_hover_callbacks(app, fig)

    app.run(port=port)
