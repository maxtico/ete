from dash import html


def tree_select(tree_name):
    return html.Div(
        [
            html.Div(
                [
                    html.Span("tree", className="dashview-control-label"),
                    html.Button(
                        tree_name,
                        id="tree-toggle",
                        className="dashview-tree-current",
                        type="button",
                    ),
                ],
                className="dashview-tree-row",
            ),
            html.Div(
                [
                    html.Button(
                        tree_name,
                        id="tree-option-current",
                        className="dashview-tree-option is-selected",
                        type="button",
                    )
                ],
                id="tree-options",
                className="dashview-tree-options",
                style={"display": "none"},
            ),
        ],
        className="dashview-tree-select",
    )


def shape_select():
    return html.Div(
        [
            html.Div(
                [
                    html.Span("shape", className="dashview-control-label"),
                    html.Button(
                        "rectangular",
                        id="shape-toggle",
                        className="dashview-tree-current dashview-shape-current",
                        type="button",
                    ),
                ],
                className="dashview-tree-row dashview-shape-row",
            ),
            html.Div(
                [
                    html.Button(
                        "rectangular",
                        id="shape-option-rectangular",
                        className="dashview-tree-option is-selected",
                        type="button",
                    ),
                    html.Button(
                        "circular",
                        id="shape-option-circular",
                        className="dashview-tree-option",
                        type="button",
                    ),
                ],
                id="shape-options",
                className="dashview-tree-options dashview-shape-options",
                style={"display": "none"},
            ),
        ],
        className="dashview-tree-select dashview-shape-select",
    )
