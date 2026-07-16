from dash import html

from .advanced import advanced_page
from .main import main_page
from .selections import selections_page


def make_control_panel(
    tree_name="current tree",
    shape="rectangular",
    node_height_min=30,
):
    """Return the floating control panel used by the Dash tree view."""
    return html.Div(
        [
            html.Button(
                "Control panel",
                id="control-panel-toggle",
                className="dashview-panel-toggle",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Button(
                                "Main",
                                id="control-panel-tab-main",
                                className="dashview-panel-tab is-active",
                            ),
                            html.Button(
                                "Selections",
                                id="control-panel-tab-selections",
                                className="dashview-panel-tab",
                            ),
                            html.Button(
                                "Advanced",
                                id="control-panel-tab-advanced",
                                className="dashview-panel-tab",
                            ),
                        ],
                        className="dashview-panel-tabs",
                    ),
                    main_page(
                        tree_name,
                        shape=shape,
                        node_height_min=node_height_min,
                    ),
                    selections_page(),
                    advanced_page(),
                ],
                id="control-panel-body",
                className="dashview-panel-body",
                style={"display": "none"},
            ),
        ],
        id="control-panel",
        className="dashview-control-panel is-collapsed",
    )
