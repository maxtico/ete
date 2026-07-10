from dash import ALL, Input, Output, State, callback_context


TAB_CLASS = "dashview-panel-tab"
ACTIVE_TAB_CLASS = "dashview-panel-tab is-active"


def _active_tab_from_classes(main_class, selections_class, advanced_class):
    if "is-active" in (selections_class or ""):
        return "selections"
    if "is-active" in (advanced_class or ""):
        return "advanced"
    return "main"


def _tab_state(active_tab):
    tab_classes = {
        "main": TAB_CLASS,
        "selections": TAB_CLASS,
        "advanced": TAB_CLASS,
    }
    tab_classes[active_tab] = ACTIVE_TAB_CLASS

    page_styles = {
        "main": {"display": "none"},
        "selections": {"display": "none"},
        "advanced": {"display": "none"},
    }
    page_styles[active_tab] = {"display": "flex"}

    return tab_classes, page_styles


def _shape_state(selected_shape):
    shape = (
        selected_shape
        if selected_shape in {"rectangular", "circular"}
        else "rectangular"
    )
    return (
        shape,
        "dashview-tree-option is-selected"
        if shape == "rectangular"
        else "dashview-tree-option",
        "dashview-tree-option is-selected"
        if shape == "circular"
        else "dashview-tree-option",
    )


def register_control_panel_callbacks(app):
    @app.callback(
        Output("control-panel", "className"),
        Output("control-panel-body", "style"),
        Output("download-options", "style"),
        Output("control-panel-tab-main", "className"),
        Output("control-panel-tab-selections", "className"),
        Output("control-panel-tab-advanced", "className"),
        Output("control-panel-page-main", "style"),
        Output("control-panel-page-selections", "style"),
        Output("control-panel-page-advanced", "style"),
        Output("tree-options", "style"),
        Output("shape-options", "style"),
        Output("shape-toggle", "children"),
        Output("shape-option-rectangular", "className"),
        Output("shape-option-circular", "className"),
        Input("control-panel-toggle", "n_clicks"),
        Input("download-toggle", "n_clicks"),
        Input("tree-toggle", "n_clicks"),
        Input({"type": "tree-option", "name": ALL}, "n_clicks"),
        Input("shape-toggle", "n_clicks"),
        Input("shape-option-rectangular", "n_clicks"),
        Input("shape-option-circular", "n_clicks"),
        Input("control-panel-tab-main", "n_clicks"),
        Input("control-panel-tab-selections", "n_clicks"),
        Input("control-panel-tab-advanced", "n_clicks"),
        State("control-panel-tab-main", "className"),
        State("control-panel-tab-selections", "className"),
        State("control-panel-tab-advanced", "className"),
        State("tree-options", "style"),
        State("shape-options", "style"),
        State("shape-toggle", "children"),
    )
    def toggle_control_panel(
        panel_clicks,
        download_clicks,
        tree_clicks,
        tree_option_clicks,
        shape_clicks,
        rectangular_clicks,
        circular_clicks,
        main_clicks,
        selections_clicks,
        advanced_clicks,
        main_class,
        selections_class,
        advanced_class,
        tree_options_style,
        shape_options_style,
        selected_shape,
    ):
        panel_is_open = bool(panel_clicks and panel_clicks % 2)
        download_is_open = bool(download_clicks and download_clicks % 2)
        tree_options_open = (tree_options_style or {}).get("display") == "block"
        shape_options_open = (shape_options_style or {}).get("display") == "block"
        active_tab = _active_tab_from_classes(
            main_class,
            selections_class,
            advanced_class,
        )

        triggered_id = callback_context.triggered_id
        if triggered_id == "control-panel-tab-main":
            active_tab = "main"
            tree_options_open = False
            shape_options_open = False
        elif triggered_id == "control-panel-tab-selections":
            active_tab = "selections"
            tree_options_open = False
            shape_options_open = False
        elif triggered_id == "control-panel-tab-advanced":
            active_tab = "advanced"
            tree_options_open = False
            shape_options_open = False
        elif triggered_id == "tree-toggle":
            tree_options_open = not tree_options_open
            shape_options_open = False
        elif isinstance(triggered_id, dict) and triggered_id.get("type") == "tree-option":
            tree_options_open = False
        elif triggered_id == "shape-toggle":
            shape_options_open = not shape_options_open
            tree_options_open = False
        elif triggered_id == "shape-option-rectangular":
            selected_shape = "rectangular"
            shape_options_open = False
        elif triggered_id == "shape-option-circular":
            selected_shape = "circular"
            shape_options_open = False

        tab_classes, page_styles = _tab_state(active_tab)
        selected_shape, rectangular_class, circular_class = _shape_state(
            selected_shape
        )

        panel_class = "dashview-control-panel"
        if not panel_is_open:
            panel_class += " is-collapsed"

        return (
            panel_class,
            {"display": "block" if panel_is_open else "none"},
            {"display": "flex" if panel_is_open and download_is_open else "none"},
            tab_classes["main"],
            tab_classes["selections"],
            tab_classes["advanced"],
            page_styles["main"],
            page_styles["selections"],
            page_styles["advanced"],
            {"display": "block" if panel_is_open and tree_options_open else "none"},
            {"display": "block" if panel_is_open and shape_options_open else "none"},
            selected_shape,
            rectangular_class,
            circular_class,
        )
