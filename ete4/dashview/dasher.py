# ete4/dashview/tree_dash.py
from ete4 import PhyloTree
from .app import run_dash_app
from .draw import tree_to_plotly

def dash(self, port=8050, export=False):
    """
    Run the Dash interactive tree explorer for this tree instance.

    Parameters:
    - port: Dash server port (default: 8050)
    - export: if True, no server is opened; returns the Plotly figure and layout.

    Example:
        t.dash(port=8050)          # opens the Dash server
        fig, layout = t.dash(export=True)  # returns the figure for use in another dashboard
    """
    if export:
        fig = tree_to_plotly(self)
        return fig
    else:
        run_dash_app(self, port=port)

# Patch direct to PhyloTree
PhyloTree.dash = dash