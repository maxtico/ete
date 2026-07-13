import pytest

pytest.importorskip("dash")
pytest.importorskip("plotly")

from ete4 import PhyloTree
from ete4.dashview.app import make_app_layout
from ete4.dashview.config import make_tree_view_config, normalize_shape
from ete4.dashview.dasher import dash
from ete4.dashview.draw import tree_to_plotly


def component_by_id(component, component_id):
    if getattr(component, "id", None) == component_id:
        return component

    children = getattr(component, "children", None)
    if children is None:
        return None
    if not isinstance(children, (list, tuple)):
        children = [children]

    for child in children:
        found = component_by_id(child, component_id)
        if found is not None:
            return found
    return None


def test_shape_config_validation():
    assert make_tree_view_config("circular") == {"shape": "circular"}
    assert normalize_shape(None) == "rectangular"
    with pytest.raises(ValueError, match="unknown tree shape"):
        normalize_shape("radial")


def test_circular_shape_initializes_figure_panel_and_store():
    tree = PhyloTree("(A:1,B:1);")
    figure = dash(tree, export=True, shape="circular")
    layout = make_app_layout(figure, shape="circular")

    assert figure.layout.meta["shape"] == "circular"
    assert component_by_id(layout, "shape-toggle").children == "circular"
    assert component_by_id(layout, "tree-view-config").data == {
        "shape": "circular"
    }
