from ete4.dashview.app import run_dash_app
from .common import src_tree_iterator
from ete4 import PhyloTree

DESC = """\
Run an interactive tree explorer using Plotly Dash.

This tool launches a web-based interactive visualization
of phylogenetic trees.
"""

def populate_parser(parser):
    # ❗ NO definim -t aquí
    # -t ja ve del source_args_p del CLI principal d’ETE

    parser.add_argument(
        "--port",
        type=int,
        default=8050,
        help="Dash server port"
    )

def run(args):
    # Obtenim arbres des de la font (-t, stdin, pipes, etc.)
    tfile = next(src_tree_iterator(args))
    t = PhyloTree(open(tfile), parser=args.src_newick_format)

    run_dash_app(t, port=args.port)
