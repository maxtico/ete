from dash import html

from .helpers import button, control, faux_button, folder, page
from .selectors import shape_select, tree_select


def main_page(tree_name, shape="rectangular"):
    return page(
        "",
        [
            tree_select(tree_name),
            html.Div(
                [
                    button(
                        "download",
                        id="download-toggle",
                        className="dashview-panel-button dashview-download-toggle",
                    ),
                    html.Div(
                        [
                            button(
                                "newick",
                                id="download-newick-button",
                                className="dashview-panel-button dashview-download-option",
                            ),
                            button(
                                "svg",
                                id="download-svg-button",
                                className="dashview-panel-button dashview-download-option",
                            ),
                            button(
                                "image",
                                id="download-image-button",
                                className="dashview-panel-button dashview-download-option",
                            ),
                        ],
                        id="download-options",
                        className="dashview-folder-body dashview-download-options",
                    ),
                ],
                className="dashview-folder dashview-download-folder is-open",
            ),
            faux_button("upload", id="upload-open"),
            shape_select(shape),
            control("node height min", ""),
            control("content height min", ""),
            folder("layouts"),
            folder(
                "extra labels",
                [
                    folder(
                        "properties",
                        [
                            control("properties", ""),
                            faux_button("add property"),
                        ],
                        open=True,
                    ),
                    faux_button("add expression"),
                ],
            ),
            control("select text", "false"),
            control("smart zoom", "true"),
            faux_button("share view"),
            faux_button("fullscreen"),
            faux_button("help"),
        ],
        page_id="control-panel-page-main",
        visible=True,
    )
