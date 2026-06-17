# ete4/dashview/app.py

from copy import deepcopy

from dash import Dash, Input, Output, dcc, html
from .draw import tree_to_plotly


def run_dash_app(tree, port=8050):
    fig = tree_to_plotly(tree)

    app = Dash(__name__)
    app.index_string = """<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            html, body, #react-entry-point {
                width: 100%;
                height: 100%;
                margin: 0;
            }
            .dashview-control-panel {
                position: fixed;
                top: 8px;
                left: 8px;
                z-index: 10000;
                width: 176px;
                border: 1px solid #dedede;
                border-radius: 10px;
                background: #dedede;
                box-shadow: 0 8px 22px rgba(0, 0, 0, 0.18);
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
                overflow: hidden;
            }
            .dashview-control-panel.is-collapsed {
                width: 120px;
                height: 21px;
            }
            .dashview-panel-toggle,
            .dashview-panel-button,
            .dashview-download-option {
                border: 0;
                background: transparent;
                color: #242424;
                cursor: pointer;
                font: inherit;
            }
            .dashview-panel-toggle {
                width: 100%;
                height: 21px;
                padding: 0 4px;
                font-weight: bold;
                text-align: left;
                font-size: 11px;
                color: #464853;
                font
            }
            .dashview-control-panel.is-collapsed .dashview-panel-toggle {
                padding: 0 12px;
                text-align: center;
            }
            .dashview-panel-button {
                width: calc(100% - 16px);
                margin: 0 8px 8px;
                padding: 8px 10px;
                border-radius: 7px;
                background: #ffffff;
                box-shadow: inset 0 0 0 1px #d9d9d9;
                text-align: left;
            }
            .dashview-panel-button:hover,
            .dashview-download-option:hover,
            .dashview-panel-toggle:hover {
                background: #e7e7e7;
            }
            .dashview-download-options {
                display: flex;
                flex-direction: column;
                gap: 4px;
                padding: 0 8px 10px;
            }
            .dashview-download-option {
                padding: 7px 10px;
                border-radius: 6px;
                text-align: left;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""
    app.layout = html.Div([
        dcc.Graph(
            id="tree-graph",
            figure=fig,
            config={"responsive": True},
            clear_on_unhover=True,
            style={"width": "100%", "height": "100%"},
        ),
        html.Div(
            [
                html.Button("Control panel", id="control-panel-toggle", className="dashview-panel-toggle"),
                html.Div(
                    [
                        html.Button("Download", id="download-toggle", className="dashview-panel-button"),
                        html.Div(
                            [
                                html.Button("Newick", className="dashview-download-option"),
                                html.Button("SVG", className="dashview-download-option"),
                                html.Button("Image", className="dashview-download-option"),
                            ],
                            id="download-options",
                            className="dashview-download-options",
                        ),
                    ],
                    id="control-panel-body",
                    style={"display": "none"},
                ),
            ],
            id="control-panel",
            className="dashview-control-panel is-collapsed",
        ),
    ], style={"position": "fixed", "inset": 0})

    @app.callback(
        Output("control-panel", "className"),
        Output("control-panel-body", "style"),
        Output("download-options", "style"),
        Input("control-panel-toggle", "n_clicks"),
        Input("download-toggle", "n_clicks"),
    )
    def toggle_control_panel(panel_clicks, download_clicks):
        panel_is_open = bool(panel_clicks and panel_clicks % 2)
        download_is_open = bool(download_clicks and download_clicks % 2)

        panel_class = "dashview-control-panel"
        if not panel_is_open:
            panel_class += " is-collapsed"

        return (
            panel_class,
            {"display": "block" if panel_is_open else "none"},
            {"display": "flex" if panel_is_open and download_is_open else "none"},
        )

    @app.callback(
        Output("tree-graph", "figure"),
        Input("tree-graph", "hoverData"),
    )
    def highlight_clade(hover_data):
        figure = deepcopy(fig)
        if not hover_data or not hover_data.get("points"):
            return figure

        point = hover_data["points"][0]
        data = point.get("customdata")
        if not data:
            return figure

        x0 = data.get("node_x", 0)
        x1 = figure.layout.xaxis.range[1]
        y0 = data.get("y_min", 0) - 0.45
        y1 = data.get("y_max", 0) + 0.45
        highlight_shape = {
            "type": "rect",
            "xref": "x",
            "yref": "y",
            "x0": x0,
            "x1": x1,
            "y0": y0,
            "y1": y1,
            "fillcolor": "rgba(210, 210, 210, 0.35)",
            "line": {"width": 0},
            "layer": "below",
        }
        figure.layout.shapes = (highlight_shape,) + tuple(figure.layout.shapes or ())
        return figure

    app.run(port=port)
