from .helpers import control, faux_button, folder, page


def advanced_page():
    return page(
        "Advanced",
        [
            control("subtree", ""),
            folder(
                "sort",
                [
                    control("key", ""),
                    control("reverse", "false"),
                    faux_button("apply"),
                ],
            ),
            folder(
                "circular",
                [
                    control("radius", ""),
                    control("angle start", ""),
                    control("angle end", ""),
                ],
            ),
            folder(
                "info",
                [
                    folder(
                        "nodes",
                        [
                            control("visible", ""),
                            control("total", ""),
                            control("leaves", ""),
                        ],
                        open=True,
                    ),
                    folder(
                        "pointer position",
                        [
                            control("x", ""),
                            control("y", ""),
                        ],
                        open=True,
                    ),
                    faux_button("show details"),
                ],
            ),
            folder(
                "viewport",
                [
                    faux_button("reset view"),
                    folder("aligned bar", [control("position", "")]),
                ],
            ),
            folder(
                "zoom",
                [
                    control("sensitivity", ""),
                    control("smart zoom", "true"),
                ],
            ),
            folder(
                "tree style",
                [
                    faux_button("use original style"),
                    folder(
                        "node",
                        [
                            folder(
                                "box",
                                [
                                    control("opacity", ""),
                                    control("color", ""),
                                ],
                                open=True,
                            ),
                            folder(
                                "dot",
                                [
                                    control("shape", ""),
                                    control("radius", ""),
                                    control("opacity", ""),
                                    control("color", ""),
                                ],
                                open=True,
                            ),
                        ],
                    ),
                    folder(
                        "collapsed",
                        [
                            control("shape", ""),
                            control("opacity", ""),
                            control("color", ""),
                            control("width", ""),
                        ],
                    ),
                    folder(
                        "lines",
                        [
                            folder(
                                "hz (horizontal/length)",
                                [
                                    control("color", ""),
                                    control("width", ""),
                                ],
                                open=True,
                            ),
                            folder(
                                "vt (vertical/children)",
                                [
                                    control("color", ""),
                                    control("width", ""),
                                    control("pattern", ""),
                                ],
                                open=True,
                            ),
                        ],
                    ),
                    folder("text", [control("automatic size", "true")]),
                    folder(
                        "sequence",
                        [
                            control("render", "auto"),
                            control("padding", ""),
                        ],
                    ),
                    folder("legend", [control("show legend", "false")]),
                ],
            ),
            folder(
                "minimap",
                [
                    control("width", ""),
                    control("height", ""),
                    control("show", "false"),
                ],
            ),
        ],
        page_id="control-panel-page-advanced",
    )
