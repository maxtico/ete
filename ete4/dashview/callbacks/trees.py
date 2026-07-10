from dash import ALL, Input, Output, State, callback_context, no_update

from ..components.control_panel_parts.selectors import tree_options


def register_tree_callbacks(app):
    @app.callback(
        Output("tree-toggle", "children"),
        Output("tree-options", "children"),
        Input("tree-names", "data"),
        Input("selected-tree", "data"),
    )
    def render_tree_selector(names, selected_name):
        names = names or []
        if selected_name not in names and names:
            selected_name = names[0]
        return selected_name or "", tree_options(names, selected_name)

    @app.callback(
        Output("selected-tree", "data"),
        Input({"type": "tree-option", "name": ALL}, "n_clicks"),
        Input("upload-result", "data"),
        State("selected-tree", "data"),
        prevent_initial_call=True,
    )
    def select_tree(option_clicks, upload_result, selected_name):
        triggered_id = callback_context.triggered_id
        if triggered_id == "upload-result":
            return upload_result.get("name") if upload_result else no_update
        if isinstance(triggered_id, dict) and triggered_id.get("type") == "tree-option":
            return triggered_id["name"]
        return selected_name
