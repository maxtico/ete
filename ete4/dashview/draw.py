import math

import plotly.graph_objects as go
from .graphics import compute_x_positions, compute_y_positions, is_leaf
from .layout import Layout, BASIC_LAYOUT


def tree_to_plotly(
    tree,
    highlight=None,
    layout=None,
    is_leaf_fn=None,
    collapsed_nodes=None,
    debug=False,
    shape="rectangular",
):
    """
    Converteix un arbre ETE a una figura Plotly.
    
    Paràmetres:
    - tree: arbre ETE
    - highlight: llista de noms de fulles a destacar
    - layout: Layout object (metadades/estils)
    - is_leaf_fn: funció que determina si un node és considerat fulla
    - collapsed_nodes: set de nodes col·lapsats
    - debug: si True imprimeix nodes sense posició
    """

    highlight = highlight or []
    layout = layout or BASIC_LAYOUT
    collapsed_nodes = collapsed_nodes or set()

    # ---------- Compute positions ----------
    y_pos = compute_y_positions(tree, is_leaf_fn=is_leaf_fn, collapsed_nodes=collapsed_nodes)
    x_pos = compute_x_positions(tree)

    if shape not in {"rectangular", "circular"}:
        shape = "rectangular"

    # ---------- Evolutionary distance ----------
    max_x = max(x_pos.values()) if x_pos else 0
    if max_x <= 0.1:
        scale_len = 0.01
    elif max_x <= 0.5:
        scale_len = 0.05
    elif max_x <= 1:
        scale_len = 0.1
    elif max_x <= 5:
        scale_len = 0.5
    else:
        scale_len = 1.0

    # ---------- Prepare figure ----------
    fig = go.Figure()
    x_lines, y_lines, line_data, line_text = [], [], [], []

    def is_visible_leaf(node):
        node_is_leaf = is_leaf_fn(node) if is_leaf_fn else is_leaf(node)
        return node_is_leaf or node in collapsed_nodes

    def get_visible_leaves(node):
        if is_visible_leaf(node):
            return [node]

        leaves = []
        for child in getattr(node, "children", []):
            leaves.extend(get_visible_leaves(child))
        return leaves

    def get_node_info(node):
        node_is_leaf = is_leaf_fn(node) if is_leaf_fn else is_leaf(node)
        leaves = get_visible_leaves(node)
        leaf_y = [y_pos.get(leaf, 0) for leaf in leaves]
        info = {
            "type": "leaf" if node_is_leaf or node in collapsed_nodes else "internal",
            "name": getattr(node, "name", "") or "",
            "dist": getattr(node, "dist", None),
            "support": getattr(node, "support", None),
            "leaf_names": [getattr(leaf, "name", "") or "" for leaf in leaves],
            "node_x": x_pos.get(node, 0),
            "y_min": min(leaf_y) if leaf_y else y_pos.get(node, 0),
            "y_max": max(leaf_y) if leaf_y else y_pos.get(node, 0),
        }
        if shape == "circular":
            # Store the polar geometry with each hover target.  The callback can
            # then draw the clade sector without having to reconstruct the tree.
            info.update(
                node_radius=radius_for_x(info["node_x"]),
                angle_start=angle_for_y(info["y_max"] + 0.5),
                angle_end=angle_for_y(info["y_min"] - 0.5),
            )
        return info

    def get_hover_text(info):
        if info["type"] == "leaf":
            rows = [info["name"]] if info["name"] else []
            if info["dist"] is not None:
                rows.append(f"dist: {info['dist']}")
            return "<br>".join(rows)
        rows = []
        if info["name"]:
            rows.append(info["name"])
        if info["dist"] is not None:
            rows.append(f"dist: {info['dist']}")
        if info["support"] is not None:
            rows.append(f"support: {info['support']}")
        return "<br>".join(rows)

    visible_leaves = [
        n for n in getattr(tree, 'traverse', lambda: [])()
        if is_visible_leaf(n)
    ]

    n_visible_leaves = max(len(visible_leaves), 1)
    circular_inner_radius = max(max_x * 0.04, scale_len * 0.5)
    circular_label_step = max(max_x * 0.012, scale_len * 0.04)
    circular_label_font_size = 12
    circular_label_pixel_gap = 8
    circular_label_pixel_char_width = circular_label_font_size * 0.56

    def angle_for_y(y):
        return math.pi - (2 * math.pi * (y + 0.5) / n_visible_leaves)

    def radius_for_x(x):
        return x + circular_inner_radius

    def polar_to_xy(radius, angle):
        return radius * math.cos(angle), radius * math.sin(angle)

    def circular_label_style(angle):
        text_angle = -math.degrees(angle)
        if text_angle < -90:
            text_angle += 180
        elif text_angle > 90:
            text_angle -= 180
        return text_angle

    def add_circular_label_annotations(annotations, text, x, y, angle):
        text_angle = circular_label_style(angle)
        label_pixel_width = len(text) * circular_label_pixel_char_width
        label_pixel_offset = circular_label_pixel_gap + label_pixel_width / 2
        annotations.append(
            dict(
                x=x,
                y=y,
                xshift=label_pixel_offset * math.cos(angle),
                yshift=label_pixel_offset * math.sin(angle),
                text=text,
                showarrow=False,
                textangle=text_angle,
                xanchor="center",
                yanchor="middle",
                font=dict(size=circular_label_font_size, color="#111"),
            )
        )
    def add_line(points, data, text):
        for x, y in points:
            x_lines.append(x)
            y_lines.append(y)
            line_data.append(data)
            line_text.append(text)
        x_lines.append(None)
        y_lines.append(None)
        line_data.append(None)
        line_text.append(None)

    def add_arc(radius, angle_start, angle_end, data, text):
        if angle_start > angle_end:
            angle_start, angle_end = angle_end, angle_start

        steps = max(12, int(abs(angle_end - angle_start) / (math.pi / 48)))
        points = [
            polar_to_xy(
                radius,
                angle_start + (angle_end - angle_start) * i / steps,
            )
            for i in range(steps + 1)
        ]
        add_line(points, data, text)

    # ---------- Draw recursive ----------
    def draw_rectangular(node):
        nonlocal x_lines, y_lines, line_data, line_text

        x0 = x_pos.get(node)
        y0 = y_pos.get(node)
        if x0 is None or y0 is None:
            if debug:
                print("Skipping node (no position):", getattr(node, 'name', node))
            return

        if node in collapsed_nodes:
            return

        children = [
            c for c in getattr(node, 'children', [])
            if x_pos.get(c) is not None and y_pos.get(c) is not None
        ]

        if len(children) > 1:
            child_y = [y_pos[c] for c in children]
            node_data = get_node_info(node)
            add_line(
                [(x0, min(child_y)), (x0, max(child_y))],
                node_data,
                get_hover_text(node_data),
            )

        for c in children:
            x1 = x_pos.get(c)
            y1 = y_pos.get(c)
            c_data = get_node_info(c)

            # Horizontal line
            add_line([(x0, y1), (x1, y1)], c_data, get_hover_text(c_data))

            draw_rectangular(c)

    def draw_circular(node):
        nonlocal x_lines, y_lines, line_data, line_text

        x0 = x_pos.get(node)
        y0 = y_pos.get(node)
        if x0 is None or y0 is None:
            if debug:
                print("Skipping node (no position):", getattr(node, 'name', node))
            return

        if node in collapsed_nodes:
            return

        children = [
            c for c in getattr(node, 'children', [])
            if x_pos.get(c) is not None and y_pos.get(c) is not None
        ]

        if node is tree and children:
            node_data = get_node_info(node)
            angle = angle_for_y(y0)
            add_line(
                [
                    polar_to_xy(0, angle),
                    polar_to_xy(radius_for_x(x0), angle),
                ],
                node_data,
                get_hover_text(node_data),
            )

        if len(children) > 1:
            child_angles = [angle_for_y(y_pos[c]) for c in children]
            node_data = get_node_info(node)
            add_arc(
                radius_for_x(x0),
                min(child_angles),
                max(child_angles),
                node_data,
                get_hover_text(node_data),
            )

        for c in children:
            x1 = x_pos.get(c)
            y1 = y_pos.get(c)
            angle = angle_for_y(y1)
            c_data = get_node_info(c)
            add_line(
                [
                    polar_to_xy(radius_for_x(x0), angle),
                    polar_to_xy(radius_for_x(x1), angle),
                ],
                c_data,
                get_hover_text(c_data),
            )

            draw_circular(c)

    if shape == "circular":
        draw_circular(tree)
    else:
        draw_rectangular(tree)

    # ---------- Branches ----------
    fig.add_trace(go.Scatter(
        x=x_lines,
        y=y_lines,
        mode="lines",
        customdata=line_data,
        line=dict(color="#444", width=2),
        hoverinfo="none",
        showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=x_lines,
        y=y_lines,
        mode="lines",
        customdata=line_data,
        text=line_text,
        line=dict(color="rgba(80, 80, 80, 0.01)", width=16),
        hoverinfo="text",
        hoverlabel=dict(bgcolor="white", bordercolor="#999", font=dict(color="#222")),
        showlegend=False
    ))

    # ---------- Leaves ----------
    leaf_x, leaf_y, leaf_text, leaf_hover, leaf_color, leaf_data = [], [], [], [], [], []
    leaf_textposition = []
    leaf_annotations = []

    for leaf in visible_leaves:
        raw_lx = x_pos.get(leaf, 0)
        raw_ly = y_pos.get(leaf, 0)
        lx = raw_lx
        ly = raw_ly
        leaf_name = getattr(leaf, 'name', '') or ''
        if shape == "circular":
            angle = angle_for_y(ly)
            leaf_radius = radius_for_x(lx)
            lx, ly = polar_to_xy(leaf_radius, angle)
            if leaf_name:
                add_circular_label_annotations(
                    leaf_annotations,
                    leaf_name,
                    lx,
                    ly,
                    angle,
                )
        else:
            leaf_textposition.append("middle right")
        leaf_x.append(lx)
        leaf_y.append(ly)

        leaf_info = get_node_info(leaf)
        leaf_text.append(leaf_name)
        leaf_hover.append(get_hover_text(leaf_info))
        leaf_color.append("crimson" if leaf_name in highlight else "#1f77b4")
        leaf_data.append(leaf_info)

    fig.add_trace(go.Scatter(
        x=leaf_x,
        y=leaf_y,
        mode="markers" if shape == "circular" else "markers+text",
        text=None if shape == "circular" else leaf_text,
        hovertext=leaf_hover,
        customdata=leaf_data,
        textposition=None if shape == "circular" else leaf_textposition,
        marker=dict(size=10, color=leaf_color),
        textfont=dict(color="#111"),
        hoverinfo="text",
        cliponaxis=False,
        showlegend=False
    ))

    max_label_len = max((len(text) for text in leaf_text), default=0)
    right_margin = max(180, min(360, max_label_len * 8 + 40))
    x_padding = max(max_x * 0.25, scale_len * 0.5)
    y_max = max(y_pos.values())
    y_bar = y_max + 1.5

    if shape == "circular":
        outer_radius = max_x + circular_inner_radius
        label_extent = max_label_len * circular_label_step
        axis_limit = max(
            (outer_radius + label_extent) * 1.04,
            scale_len * 1.2,
        )
        xaxis = dict(
            showticklabels=False,
            ticks="",
            showgrid=False,
            zeroline=False,
            range=[-axis_limit, axis_limit],
            scaleanchor="y",
            scaleratio=1,
        )
        yaxis = dict(
            showticklabels=False,
            ticks="",
            showgrid=False,
            zeroline=False,
            range=[-axis_limit, axis_limit],
        )
        margin = dict(l=60, r=60, t=40, b=40)
    else:
        xaxis = dict(
            showticklabels=False,
            ticks="",
            showgrid=False,
            zeroline=False,
            range=[0, max(max_x, scale_len) + x_padding],
        )
        yaxis = dict(
            showticklabels=False,
            range=[y_bar + 1, -1],
        )
        right_margin = max(180, min(360, max_label_len * 8 + 40))
        margin = dict(l=40, r=right_margin, t=20, b=40)

    if shape == "circular":
        fig.update_layout(annotations=leaf_annotations)

    # ---------- Layout ----------
    fig.update_layout(
        autosize=True,
        margin=margin,
        xaxis=xaxis,
        yaxis=yaxis,
        plot_bgcolor="white",
        clickmode="event+select",
        uirevision=f"dashview-tree-{shape}",
        meta={"shape": shape},
    )

    if debug:
        missing = [n for n in x_pos if x_pos[n] is None or y_pos[n] is None]
        if missing:
            print("Nodes without position:", missing)

    if shape == "circular":
        return fig

    # --------- Drawing evolutionary distance ----------
    # Drawing evolutionary distance bar
    fig.add_shape(
        type="line",
        x0=0,
        x1=scale_len,
        y0=y_bar,
        y1=y_bar,
        line=dict(color="black", width=2),
        layer="below"
    )
    fig.add_shape(
        type="line",
        x0=0,
        x1=0,
        y0=y_bar - 0.8,
        y1=y_bar + 0.8,
        line=dict(color="black", width=2),
        layer="below"
    )
    fig.add_shape(
        type="line",
        x0=scale_len,
        x1=scale_len,
        y0=y_bar - 0.8,
        y1=y_bar + 0.8,
        line=dict(color="black", width=2),
        layer="below"
    )
    fig.add_annotation(
        x=scale_len / 2,
        y=y_bar-1.1,        # una mica per sota
        text=str(scale_len),
        showarrow=False,
        font=dict(size=12, color="black"),
        xanchor="center",
        yanchor="top",
        hovertext=None,
        captureevents=False
    )

    return fig
