from dash import dcc


def make_tree_graph(fig):
    return dcc.Graph(
        id="tree-graph",
        figure=fig,
        config={"responsive": True},
        clear_on_unhover=True,
        style={"width": "100%", "height": "100%"},
    )

