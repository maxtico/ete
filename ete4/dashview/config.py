VALID_SHAPES = {"rectangular", "circular"}
DEFAULT_SHAPE = "rectangular"


def normalize_shape(shape):
    """Return a supported tree shape, using the default for falsey values."""
    shape = shape or DEFAULT_SHAPE
    if shape not in VALID_SHAPES:
        choices = ", ".join(sorted(VALID_SHAPES))
        raise ValueError(f"unknown tree shape {shape!r}; expected one of: {choices}")
    return shape


def make_tree_view_config(shape=DEFAULT_SHAPE):
    """Return JSON-serializable state shared by the renderer and Dash UI."""
    return {"shape": normalize_shape(shape)}
