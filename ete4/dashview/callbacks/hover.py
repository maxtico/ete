import math

from dash import Input, Output, callback_context

from ..config import normalize_shape
from ..draw import tree_to_plotly


def _annular_sector_path(inner_radius, outer_radius, angle_start, angle_end):
    """Return a Plotly SVG path for an annular sector."""
    angle_start, angle_end = sorted((angle_start, angle_end))
    steps = max(12, int(abs(angle_end - angle_start) / (math.pi / 48)))
    angles = [
        angle_start + (angle_end - angle_start) * i / steps
        for i in range(steps + 1)
    ]

    outer = [
        (outer_radius * math.cos(angle), outer_radius * math.sin(angle))
        for angle in angles
    ]
    inner = [
        (inner_radius * math.cos(angle), inner_radius * math.sin(angle))
        for angle in reversed(angles)
    ]
    points = outer + inner
    commands = [f"M {points[0][0]:.12g},{points[0][1]:.12g}"]
    commands.extend(f"L {x:.12g},{y:.12g}" for x, y in points[1:])
    commands.append("Z")
    return " ".join(commands)


def register_hover_callbacks(app, tree):
    @app.callback(
        Output("tree-graph", "figure"),
        Input("tree-graph", "hoverData"),
        Input("tree-view-config", "data"),
        Input("selected-tree", "data"),
    )
    def update_tree_figure(hover_data, tree_view_config, selected_tree):
        selected_shape = normalize_shape((tree_view_config or {}).get("shape"))
        current_tree = tree.get(selected_tree) if isinstance(tree, dict) else tree
        if current_tree is None:
            current_tree = next(iter(tree.values()))
        figure = tree_to_plotly(current_tree, shape=selected_shape)
        if callback_context.triggered_id == "selected-tree":
            return figure
        if not hover_data or not hover_data.get("points"):
            return figure

        point = hover_data["points"][0]
        data = point.get("customdata")
        if not data:
            return figure

        if selected_shape == "circular":
            geometry = (
                data.get("node_radius"),
                data.get("angle_start"),
                data.get("angle_end"),
            )
            if any(value is None for value in geometry):
                return figure

            outer_radius = figure.layout.xaxis.range[1]
            highlight_shape = {
                "type": "path",
                "path": _annular_sector_path(
                    data["node_radius"],
                    outer_radius,
                    data["angle_start"],
                    data["angle_end"],
                ),
                "xref": "x",
                "yref": "y",
                "fillcolor": "rgba(210, 210, 210, 0.35)",
                "line": {"width": 0},
                "layer": "below",
            }
            figure.layout.shapes = (highlight_shape,) + tuple(
                figure.layout.shapes or ()
            )
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
