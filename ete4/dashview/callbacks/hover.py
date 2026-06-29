from dash import Input, Output

from ..draw import tree_to_plotly


def register_hover_callbacks(app, tree):
    @app.callback(
        Output("tree-graph", "figure"),
        Input("tree-graph", "hoverData"),
        Input("shape-toggle", "children"),
    )
    def update_tree_figure(hover_data, selected_shape):
        figure = tree_to_plotly(tree, shape=selected_shape)
        if not hover_data or not hover_data.get("points"):
            return figure

        if selected_shape != "rectangular":
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
