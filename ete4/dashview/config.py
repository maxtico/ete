VALID_SHAPES = {"rectangular", "circular"}
DEFAULT_SHAPE = "rectangular"
DEFAULT_NODE_HEIGHT_MIN = 30
NODE_HEIGHT_MIN_RANGE = (1, 200)


def normalize_shape(shape):
    """Return a supported tree shape, using the default for falsey values."""
    shape = shape or DEFAULT_SHAPE
    if shape not in VALID_SHAPES:
        choices = ", ".join(sorted(VALID_SHAPES))
        raise ValueError(f"unknown tree shape {shape!r}; expected one of: {choices}")
    return shape


def normalize_node_height_min(value):
    """Return a valid minimum node height in pixels."""
    if value is None:
        return DEFAULT_NODE_HEIGHT_MIN
    try:
        value = int(value)
    except (TypeError, ValueError) as error:
        raise ValueError("node_height_min must be an integer") from error

    minimum, maximum = NODE_HEIGHT_MIN_RANGE
    if not minimum <= value <= maximum:
        raise ValueError(
            f"node_height_min must be between {minimum} and {maximum}"
        )
    return value


def make_tree_view_config(
    shape=DEFAULT_SHAPE,
    node_height_min=DEFAULT_NODE_HEIGHT_MIN,
):
    """Return JSON-serializable state shared by the renderer and Dash UI."""
    return {
        "shape": normalize_shape(shape),
        "node_height_min": normalize_node_height_min(node_height_min),
    }
