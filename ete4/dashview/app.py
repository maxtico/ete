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
        )
    ], style={"position": "fixed", "inset": 0})

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
        highlight_trace = figure.data[0]
        highlight_trace.x = [x0, x1, x1, x0, x0]
        highlight_trace.y = [y0, y0, y1, y1, y0]
        return figure

    app.run(port=port)
