from dash import Input, Output, State, callback_context


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
        Input("control-panel-toggle", "n_clicks"),
        Input("download-toggle", "n_clicks"),
        Input("tree-toggle", "n_clicks"),
        Input("tree-option-current", "n_clicks"),
        Input("control-panel-tab-main", "n_clicks"),
        Input("control-panel-tab-selections", "n_clicks"),
        Input("control-panel-tab-advanced", "n_clicks"),
        State("control-panel-tab-main", "className"),
        State("control-panel-tab-selections", "className"),
        State("control-panel-tab-advanced", "className"),
        State("tree-options", "style"),
    )
    def toggle_control_panel(
        panel_clicks,
        download_clicks,
        tree_clicks,
        tree_option_clicks,
        main_clicks,
        selections_clicks,
        advanced_clicks,
        main_class,
        selections_class,
        advanced_class,
        tree_options_style,
    ):
        panel_is_open = bool(panel_clicks and panel_clicks % 2)
        download_is_open = bool(download_clicks and download_clicks % 2)
        tree_options_open = (tree_options_style or {}).get("display") == "block"
        active_tab = _active_tab_from_classes(
            main_class,
            selections_class,
            advanced_class,
        )

        triggered_id = callback_context.triggered[0]["prop_id"].split(".")[0]
        if triggered_id == "control-panel-tab-main":
            active_tab = "main"
            tree_options_open = False
        elif triggered_id == "control-panel-tab-selections":
            active_tab = "selections"
            tree_options_open = False
        elif triggered_id == "control-panel-tab-advanced":
            active_tab = "advanced"
            tree_options_open = False
        elif triggered_id == "tree-toggle":
            tree_options_open = not tree_options_open
        elif triggered_id == "tree-option-current":
            tree_options_open = False

        tab_classes, page_styles = _tab_state(active_tab)

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
        )
