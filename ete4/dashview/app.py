from dash import Dash, dcc, html

from .callbacks.control_panel import register_control_panel_callbacks
from .callbacks.downloads import register_download_callbacks
from .callbacks.hover import register_hover_callbacks
from .callbacks.trees import register_tree_callbacks
from .callbacks.upload import register_upload_callbacks
from .components.control_panel import CONTROL_PANEL_STYLE, make_control_panel
from .components.upload_page import UPLOAD_STYLE, make_upload_page
from .components.tree_graph import make_tree_graph
from .config import (
    DEFAULT_NODE_HEIGHT_MIN,
    DEFAULT_SHAPE,
    make_tree_view_config,
    normalize_node_height_min,
    normalize_shape,
)
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
{BASE_STYLE}{CONTROL_PANEL_STYLE}{UPLOAD_STYLE}
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


def make_app_layout(
    fig,
    tree_name="current tree",
    shape=DEFAULT_SHAPE,
    node_height_min=DEFAULT_NODE_HEIGHT_MIN,
):
    shape = normalize_shape(shape)
    node_height_min = normalize_node_height_min(node_height_min)
    return html.Div(
        [
            html.Div(
                [
                    make_tree_graph(fig),
                    make_control_panel(
                        tree_name,
                        shape=shape,
                        node_height_min=node_height_min,
                    ),
                ],
                id="dashboard-page",
                style={"position": "fixed", "inset": 0, "display": "block"},
            ),
            make_upload_page(),
            dcc.Download(id="download-newick"),
            dcc.Store(id="download-svg-trigger"),
            dcc.Store(id="download-image-trigger"),
            dcc.Store(id="tree-names", data=[tree_name]),
            dcc.Store(id="selected-tree", data=tree_name),
            dcc.Store(id="upload-result"),
            dcc.Store(
                id="tree-view-config",
                data=make_tree_view_config(shape, node_height_min),
            ),
        ],
    )


def run_dash_app(
    tree,
    port=8050,
    tree_name="current tree",
    shape=DEFAULT_SHAPE,
):
    shape = normalize_shape(shape)
    fig = tree_to_plotly(tree, shape=shape)
    trees = {tree_name: tree}

    app = Dash(__name__)
    app.index_string = make_index_string()
    app.layout = make_app_layout(fig, tree_name, shape=shape)

    register_control_panel_callbacks(app)
    register_tree_callbacks(app)
    register_upload_callbacks(app, trees)
    register_download_callbacks(app, trees)
    register_hover_callbacks(app, trees)

    app.run(port=port)
