# draw.py
import plotly.graph_objects as go
from .graphics import compute_x_positions, compute_y_positions
from .layout import Layout, BASIC_LAYOUT

def tree_to_plotly(tree, highlight=None, layout=None, is_leaf_fn=None, collapsed_nodes=None, debug=False):
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

    # ---------- Evolutionary distance ----------
    max_x = max(x_pos.values()) if x_pos else 0

    # ---------- Prepare figure ----------
    fig = go.Figure()
    x_lines, y_lines = [], []

    # ---------- Draw recursive ----------
    def draw(node):
        nonlocal x_lines, y_lines

        x0 = x_pos.get(node)
        y0 = y_pos.get(node)
        if x0 is None or y0 is None:
            if debug:
                print("Skipping node (no position):", getattr(node, 'name', node))
            return

        if node in collapsed_nodes:
            return

        for c in getattr(node, 'children', []):
            x1 = x_pos.get(c)
            y1 = y_pos.get(c)
            if x1 is None or y1 is None:
                if debug:
                    print("Skipping child node (no position):", getattr(c, 'name', c))
                continue

            # Vertical line
            x_lines += [x0, x0, None]
            y_lines += [y0, y1, None]

            # Horizontal line
            x_lines += [x0, x1, None]
            y_lines += [y1, y1, None]

            draw(c)

    draw(tree)

    # ---------- Branches ----------
    fig.add_trace(go.Scatter(
        x=x_lines,
        y=y_lines,
        mode="lines",
        line=dict(color="#444", width=2),
        hoverinfo="none",
        showlegend=False
    ))

    # ---------- Leaves ----------
    leaf_x, leaf_y, leaf_text, leaf_color = [], [], [], []

    leaves = list(getattr(tree, 'leaves', lambda: [])())
    for leaf in leaves:
        lx = x_pos.get(leaf, 0)
        ly = y_pos.get(leaf, 0)
        leaf_x.append(lx)
        leaf_y.append(ly)

        leaf_name = getattr(leaf, 'name', '') or ''
        leaf_text.append(leaf_name)
        leaf_color.append("crimson" if leaf_name in highlight else "#1f77b4")

    fig.add_trace(go.Scatter(
        x=leaf_x,
        y=leaf_y,
        mode="markers+text",
        text=leaf_text,
        textposition="middle right",
        marker=dict(size=10, color=leaf_color),
        hoverinfo="text",
        showlegend=False
    ))

    # ---------- Layout ----------
    fig.update_layout(
        margin=dict(l=40, r=40, t=20, b=20),
        xaxis=dict(showticklabels=False,ticks="",showgrid=False,zeroline=False),
        yaxis=dict(showticklabels=False, autorange="reversed"),
        plot_bgcolor="white"
    )

    if debug:
        missing = [n for n in x_pos if x_pos[n] is None or y_pos[n] is None]
        if missing:
            print("Nodes without position:", missing)

    # --------- Drawing evolutionary distance ----------
    y_max = max(y_pos.values())
    y_bar = y_max + 1.5  # Position below the bottom leaf

    # Assigning rounded scale length
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

    # Drawing evolutionary distance bar
    fig.add_shape(
        type="line",
        x0=0,
        x1=0.01,
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
        x0=0.01,
        x1=0.01,
        y0=y_bar - 0.8,
        y1=y_bar + 0.8,
        line=dict(color="black", width=2),
        layer="below"
    )
    fig.add_annotation(
        x=0.012,      # centrat sobre la barra
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

