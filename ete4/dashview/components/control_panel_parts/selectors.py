from dash import html


def tree_options(tree_names, selected_name):
    return [
        html.Button(
            name,
            id={"type": "tree-option", "name": name},
            className=(
                "dashview-tree-option is-selected"
                if name == selected_name
                else "dashview-tree-option"
            ),
            type="button",
        )
        for name in tree_names
    ]


def tree_select(tree_name, tree_names=None):
    tree_names = tree_names or [tree_name]
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
                tree_options(tree_names, tree_name),
                id="tree-options",
                className="dashview-tree-options",
                style={"display": "none"},
            ),
        ],
        className="dashview-tree-select",
    )


def shape_select(shape="rectangular"):
    return html.Div(
        [
            html.Div(
                [
                    html.Span("shape", className="dashview-control-label"),
                    html.Button(
                        shape,
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
                        className=(
                            "dashview-tree-option is-selected"
                            if shape == "rectangular"
                            else "dashview-tree-option"
                        ),
                        type="button",
                    ),
                    html.Button(
                        "circular",
                        id="shape-option-circular",
                        className=(
                            "dashview-tree-option is-selected"
                            if shape == "circular"
                            else "dashview-tree-option"
                        ),
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
