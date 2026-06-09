from ete4.dashview.app import run_dash_app
from .common import src_tree_iterator
from ete4 import PhyloTree

DESC = """\
Run an interactive tree explorer using Plotly Dash.

This tool launches a web-based interactive visualization
of phylogenetic trees.
"""

def populate_args(parser):
    parser.add_argument(
        "--port",
        type=int,
        default=8050,
        help="Dash server port"
    )


populate_parser = populate_args


def run(args):
    tfile = next(src_tree_iterator(args))
    t = PhyloTree(open(tfile), parser=args.src_newick_format)

    run_dash_app(t, port=args.port)
