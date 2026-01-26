# graphics.py
from math import pi

def compute_y_positions(tree, is_leaf_fn=None, collapsed_nodes=None):
    """
    Assigna coordenades y a tots els nodes segons jerarquia i nodes col·lapsats.
    """
    is_leaf_fn = is_leaf_fn or (lambda n: getattr(n, 'is_leaf', False))
    collapsed_nodes = collapsed_nodes or set()
    y_pos = {}
    leaf_index = 0

    def assign_y(node):
        nonlocal leaf_index
        # Node visual: fulla real o node col·lapsat
        if is_leaf_fn(node) or node in collapsed_nodes or getattr(node,'is_leaf',False):
            y_pos[node] = leaf_index
            leaf_index += 1
        else:
            for c in getattr(node, 'children', []):
                assign_y(c)
            y_pos[node] = sum(y_pos[c] for c in getattr(node, 'children', [])) / len(getattr(node, 'children', []))

    assign_y(tree)

    # Centrar arrel verticalment
    leaves = [l for l in getattr(tree,'leaves', lambda: [])()]
    if leaves:
        all_leaf_y = [y_pos[l] for l in leaves]
        y_pos[tree] = (min(all_leaf_y) + max(all_leaf_y)) / 2

    return y_pos


def compute_x_positions(tree):
    """
    Assigna coordenades x (distància des de la arrel) a tots els nodes.
    """
    x_pos = {}

    def dist_from_root(node):
        d = 0
        n = node
        while getattr(n, 'up', None):
            d += getattr(n, 'dist', 0)
            n = getattr(n, 'up', None)
        return d

    for node in getattr(tree,'traverse', lambda: [])():
        x_pos[node] = dist_from_root(node)

    return x_pos
