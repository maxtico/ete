# ete4/dashview/app.py

from dash import Dash, dcc, html
from .draw import tree_to_plotly


def run_dash_app(tree, port=8050):
    fig = tree_to_plotly(tree)

    app = Dash(__name__)
    app.layout = html.Div([
        dcc.Graph(figure=fig)
    ])

    app.run(port=port)
