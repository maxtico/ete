# graphics.py
def compute_y_positions(tree, is_leaf_fn=None, collapsed_nodes=None):
    """
    Assigna coordenades y a tots els nodes segons jerarquia i nodes col·lapsats.
    """
    is_leaf_fn = is_leaf_fn or is_leaf
    collapsed_nodes = collapsed_nodes or set()
    y_pos = {}
    leaf_index = 0

    def assign_y(node):
        nonlocal leaf_index
        # Node visual: fulla real o node col·lapsat
        if is_leaf_fn(node) or node in collapsed_nodes:
            y_pos[node] = leaf_index
            leaf_index += 1
            return

        children = list(getattr(node, 'children', []))
        for c in children:
            assign_y(c)

        child_y = [y_pos[c] for c in children if c in y_pos]
        if child_y:
            y_pos[node] = (min(child_y) + max(child_y)) / 2
        else:
            y_pos[node] = leaf_index

    assign_y(tree)

    return y_pos


def is_leaf(node):
    leaf = getattr(node, 'is_leaf', False)
    return leaf() if callable(leaf) else bool(leaf)


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
