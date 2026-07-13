# ete4/dashview/tree_dash.py
from ete4 import PhyloTree
from .app import run_dash_app
from .config import DEFAULT_SHAPE, normalize_shape
from .draw import tree_to_plotly

def dash(self, port=8050, export=False, shape=DEFAULT_SHAPE):
    """
    Run the Dash interactive tree explorer for this tree instance.

    Parameters:
    - port: Dash server port (default: 8050)
    - export: if True, no server is opened; returns the Plotly figure.
    - shape: initial tree shape ("rectangular" or "circular").

    Example:
        t.dash(port=8050)          # opens the Dash server
        fig = t.dash(export=True, shape="circular")
    """
    shape = normalize_shape(shape)
    if export:
        fig = tree_to_plotly(self, shape=shape)
        return fig
    else:
        run_dash_app(self, port=port, shape=shape)

# Patch direct to PhyloTree
PhyloTree.dash = dash
