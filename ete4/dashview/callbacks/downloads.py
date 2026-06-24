from dash import Input, Output
from dash.exceptions import PreventUpdate
from ete4 import newick


def register_download_callbacks(app, tree):
    @app.callback(
        Output("download-newick", "data"),
        Input("download-newick-button", "n_clicks"),
        prevent_initial_call=True,
    )
    def download_newick(n_clicks):
        if not n_clicks:
            raise PreventUpdate

        return {
            "content": newick.dumps(tree),
            "filename": "tree.nw",
            "type": "text/plain",
        }

    app.clientside_callback(
        """
        function(n_clicks) {
            if (!n_clicks) {
                return window.dash_clientside.no_update;
            }

            const graph = document.getElementById("tree-graph");
            const plot = graph && (graph.querySelector(".js-plotly-plot") || graph);
            if (!plot || !window.Plotly) {
                return window.dash_clientside.no_update;
            }

            window.Plotly.downloadImage(plot, {
                format: "svg",
                filename: "tree",
                width: plot.clientWidth || 1200,
                height: plot.clientHeight || 800
            });
            return Date.now();
        }
        """,
        Output("download-svg-trigger", "data"),
        Input("download-svg-button", "n_clicks"),
        prevent_initial_call=True,
    )

    app.clientside_callback(
        """
        function(n_clicks) {
            if (!n_clicks) {
                return window.dash_clientside.no_update;
            }

            const graph = document.getElementById("tree-graph");
            const plot = graph && (graph.querySelector(".js-plotly-plot") || graph);
            if (!plot || !window.Plotly) {
                return window.dash_clientside.no_update;
            }

            window.Plotly.downloadImage(plot, {
                format: "png",
                filename: "tree",
                width: plot.clientWidth || 1200,
                height: plot.clientHeight || 800
            });
            return Date.now();
        }
        """,
        Output("download-image-trigger", "data"),
        Input("download-image-button", "n_clicks"),
        prevent_initial_call=True,
    )

