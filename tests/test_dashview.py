import pytest

pytest.importorskip("dash")
pytest.importorskip("plotly")

from ete4 import PhyloTree
from ete4.dashview.app import make_app_layout
from ete4.dashview.config import (
    make_tree_view_config,
    normalize_node_height_min,
    normalize_shape,
)
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
    assert make_tree_view_config("circular") == {
        "shape": "circular",
        "node_height_min": 30,
    }
    assert normalize_shape(None) == "rectangular"
    with pytest.raises(ValueError, match="unknown tree shape"):
        normalize_shape("radial")


def test_node_height_min_config_validation():
    assert normalize_node_height_min(None) == 30
    assert normalize_node_height_min("45") == 45
    with pytest.raises(ValueError, match="between 1 and 200"):
        normalize_node_height_min(0)


def test_node_height_min_collapses_clades_below_pixel_threshold():
    cherries = ",".join(
        f"(L{index * 2}:1,L{index * 2 + 1}:1):1"
        for index in range(40)
    )
    tree = PhyloTree(f"({cherries});")

    detailed = tree_to_plotly(tree, node_height_min=1)
    collapsed = tree_to_plotly(tree, node_height_min=30)

    assert len(detailed.data[2].x) == 80
    assert len(collapsed.data[2].x) < len(detailed.data[2].x)


def test_circular_shape_initializes_figure_panel_and_store():
    tree = PhyloTree("(A:1,B:1);")
    figure = dash(tree, export=True, shape="circular")
    layout = make_app_layout(figure, shape="circular")

    assert figure.layout.meta["shape"] == "circular"
    assert component_by_id(layout, "shape-toggle").children == "circular"
    assert component_by_id(layout, "tree-view-config").data == {
        "shape": "circular",
        "node_height_min": 30,
    }
    node_height_input = component_by_id(layout, "node-height-min-input")
    assert node_height_input.value == 30
    assert (node_height_input.min, node_height_input.max) == (1, 200)
