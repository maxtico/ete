from dash import html


CONTROL_PANEL_STYLE = """
            /* Whole floating control panel: position, size, colors, font. */
            .dashview-control-panel {
                --tp-base-font-family: sans-serif;
                --tp-base-background-color: hsla(0, 0%, 96%, 1.00);
                --tp-base-shadow-color: hsla(0, 0%, 0%, 0.1);
                --tp-button-background-color: hsla(0, 0%, 80%, 1.00);
                --tp-button-background-color-active: hsla(0, 0%, 65%, 1.00);
                --tp-button-background-color-focus: hsla(0, 0%, 70%, 1.00);
                --tp-button-background-color-hover: hsla(0, 0%, 75%, 1.00);
                --tp-button-foreground-color: hsla(230, 10%, 30%, 1.00);
                --tp-container-background-color: hsla(0, 0%, 50%, 0.20);
                --tp-container-background-color-active: hsla(0, 0%, 65%, 0.20);
                --tp-container-background-color-focus: hsla(0, 0%, 60%, 0.20);
                --tp-container-background-color-hover: hsla(0, 0%, 55%, 0.20);
                --tp-container-foreground-color: hsla(230, 10%, 30%, 1);
                --tp-groove-foreground-color: hsla(230, 15%, 30%, 0.1);
                --tp-input-background-color: hsla(230, 15%, 30%, 0.1);
                --tp-input-background-color-active: hsla(231, 15%, 45%, 0.10);
                --tp-input-background-color-focus: hsla(230, 15%, 40%, 0.10);
                --tp-input-background-color-hover: hsla(231, 15%, 35%, 0.10);
                --tp-input-foreground-color: hsla(230, 10%, 30%, 1.00);
                --tp-label-foreground-color: hsla(230, 10%, 30%, 0.7);
                --tp-monitor-background-color: hsla(230, 15%, 30%, 0.1);
                --tp-monitor-foreground-color: hsla(230, 10%, 30%, 0.5);
                position: fixed;
                top: 10px;
                left: 10px;
                z-index: 3;
                width: 276px;
                max-height: calc(100vh - 20px);
                border-radius: 6px;
                background: var(--tp-base-background-color);
                box-shadow: 0 2px 8px var(--tp-base-shadow-color);
                color: var(--tp-container-foreground-color);
                font-family: var(--tp-base-font-family);
                font-size: 11px;
                line-height: 1.2;
                overflow: hidden;
                user-select: none;
            }

            /* Collapsed panel size: the short "Control panel" bar before opening. */
            .dashview-control-panel.is-collapsed {
                width: 120px;
                height: 21px;
            }

            /* Shared button reset: applies to panel title, tabs, buttons, fake buttons. */
            .dashview-panel-toggle,
            .dashview-panel-button,
            .dashview-panel-tab,
            .dashview-faux-button {
                border: 0;
                appearance: none;
                cursor: pointer;
                font: inherit;
                font-weight: bold;
            }

            /* "Control panel" title button at the top. */
            .dashview-panel-toggle {
                display: block;
                width: 100%;
                height: 21px;
                padding: 0 8px;
                background: var(--tp-base-background-color);
                color: var(--tp-container-foreground-color);
                text-align: left;
            }

            /* Alignment of the top title while the panel is collapsed. */
            .dashview-control-panel.is-collapsed .dashview-panel-toggle {
                text-align: center;
            }

            /* Alignment of the top title while the panel is expanded. */
            .dashview-control-panel:not(.is-collapsed) .dashview-panel-toggle {
                text-align: center;
            }

            /* Triangle icons used by the top title and every folder title. */
            .dashview-panel-toggle::before,
            .dashview-folder-title::before {
                content: "";
                display: inline-block;
                width: 0;
                height: 0;
                margin: 0 7px 1px 2px;
                border-top: 4px solid transparent;
                border-bottom: 4px solid transparent;
                border-left: 6px solid var(--tp-container-foreground-color);
                vertical-align: middle;
            }

            /* Rotated triangle for expanded panel/folders. */
            .dashview-control-panel:not(.is-collapsed) .dashview-panel-toggle::before,
            .dashview-folder.is-open > .dashview-folder-title::before {
                transform: rotate(90deg);
            }

            /* Expanded panel body: contains tabs plus the active page. */
            .dashview-panel-body {
                max-height: calc(100vh - 41px);
                padding: 4px;
                border-top: 1px solid var(--tp-groove-foreground-color);
                overflow-y: auto;
            }

            /* Top tab row: Main / Selections / Advanced.
               margin-bottom controls distance from tabs to first option. */
            .dashview-panel-tabs {
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 2px;
                margin-bottom: 4px;
            }

            /* Individual tab button: Main, Selections, Advanced. */
            .dashview-panel-tab {
                min-height: 24px;
                padding: 5px 4px;
                border-radius: 4px;
                background: var(--tp-container-background-color);
                color: var(--tp-container-foreground-color);
                text-align: center;
            }

            /* Active tab button. */
            .dashview-panel-tab.is-active {
                background: var(--tp-container-background-color-hover);
            }

            /* Active page content.
               gap controls distance between top-level options:
               tree -> download, download -> upload, upload -> shape, etc. */
            .dashview-panel-page {
                flex-direction: column;
                gap: 4px;
                margin-bottom: 2px;
            }

            /* Optional page title for pages with visible titles.
               Main currently has no title element, so this affects Selections/Advanced. */
            .dashview-panel-page-title {
                margin: 6px 2px 0;
                color: var(--tp-label-foreground-color);
                font-weight: bold;
                text-transform: uppercase;
            }

            /* Folder wrapper: download folder, layouts folder, extra labels, etc. */
            .dashview-folder {
                margin-bottom: 0;
            }

            /* Whole download block: header button plus newick/svg/image submenu. */
            .dashview-download-folder {
                margin-bottom: 0;
            }

            /* Folder header row: "download", "layouts", "extra labels", etc. */
            .dashview-folder-title {
                min-height: 24px;
                padding: 5px 8px;
                border-radius: 4px;
                background: var(--tp-container-background-color);
                color: var(--tp-container-foreground-color);
                font-weight: bold;
            }

            /* Generic folder contents: shared layout for any folder's children. */
            .dashview-folder-body {
                display: flex;
                flex-direction: column;
                gap: 4px;
                padding: 4px 0 0 12px;
            }

            /* Download submenu contents only:
               controls the distance between newick -> svg -> image.
               Change gap for option spacing.
               Change padding for indentation/top space inside download. */
            .dashview-download-options {
                gap: 4px;
                padding: 4px 0 0 12px;
            }

            /* Generic label/value row: shape, node height min, smart zoom, etc. */
            .dashview-control-row {
                display: grid;
                grid-template-columns: minmax(0, 1fr) minmax(74px, 0.9fr);
                align-items: center;
                gap: 6px;
                min-height: 24px;
                padding: 2px 4px;
                color: var(--tp-label-foreground-color);
            }

            /* Right-side value box for generic rows. */
            .dashview-control-value {
                min-height: 20px;
                padding: 4px 6px;
                border-radius: 4px;
                background: var(--tp-input-background-color);
                color: var(--tp-input-foreground-color);
                overflow: hidden;
                text-align: right;
                text-overflow: ellipsis;
                white-space: nowrap;
            }

            /* Tree selector wrapper: the special clickable "tree" row. */
            .dashview-tree-select {
                position: relative;
                margin: 0;
            }

            /* Tree selector visible row: label on left, selected tree button on right. */
            .dashview-tree-row {
                display: grid;
                grid-template-columns: minmax(0, 1fr) 156px;
                align-items: center;
                gap: 6px;
                min-height: 24px;
                padding: 0 4px;
                color: var(--tp-label-foreground-color);
                font-weight: bold;
            }

            /* Right-side selected tree button, e.g. mammal_tree.nw.
               Keep this borderless; popup borders are controlled below. */
            .dashview-tree-current {
                appearance: none;
                border: 0;
                cursor: pointer;
                height: 20px;
                padding: 4px 4px;
                border-radius: 4px;
                background: #CCCCCC;
                color: var(--tp-input-foreground-color);
                font: inherit;
                font-weight: bold;
                overflow: hidden;
                text-align: left;
                text-overflow: ellipsis;
                white-space: nowrap;
            }

            /* Popup/list shown above the tree selector.
               bottom places it above the current tree button.
               right and width align it with the current tree button. */
            .dashview-tree-options {
                border: 1px solid #7C7A77;
                display: flex;
                position: absolute;
                left: 100px;
                bottom: calc(-15%);
                z-index: 2;
                width: 156px;
                border-radius: 10px;
                padding: 4px;
                box-sizing: border-box;
                background: #5C5955;
                box-shadow: 0 2px 8px var(--tp-base-shadow-color);
            }

            /* One clickable tree option button inside the popup/list. */
            .dashview-tree-option {
                appearance: none;
                border: 0;
                box-sizing: border-box;
                cursor: pointer;
                display: flex;
                align-items: center;
                width: 100%;
                min-height: 20px;
                padding: 4px 6px;
                border-radius: 10px;
                background: #5C5955;
                color: white;
                font: inherit;
                overflow: hidden;
                text-align: left;
                text-overflow: ellipsis;
                white-space: nowrap;
            }

            /* Tick marker for the selected tree option inside the popup. */
            .dashview-tree-option.is-selected::before {
                content: "\\2714";
                margin-right: 6px;
            }

            /* Hover state for tree options inside the popup/list. */
            .dashview-tree-option:hover {
                background: #507DDF;
            }

            /* Regular command buttons:
               download submenu options (newick/svg/image), upload, help, etc. */
            .dashview-panel-button,
            .dashview-faux-button {
                width: 100%;
                min-height: 24px;
                padding: 5px 8px;
                border-radius: 4px;
                background: var(--tp-button-background-color);
                color: var(--tp-button-foreground-color);
                text-align: center;
            }

            /* Individual download option buttons: newick, svg, image. */
            .dashview-download-option {
                min-height: 24px;
                padding: 5px 8px;
            }

            /* Download folder header button. */
            .dashview-download-toggle {
                background: #DEDEDE;
                text-align: left;
            }

            /* Hover state for regular command buttons. */
            .dashview-panel-button:hover,
            .dashview-faux-button:hover {
                background: var(--tp-button-background-color-hover);
            }

            /* Hover state for tabs, title bar, and folder headers. */
            .dashview-panel-tab:hover,
            .dashview-panel-toggle:hover,
            .dashview-folder-title:hover {
                background: var(--tp-container-background-color-hover);
            }

            /* Keyboard focus state for regular command buttons. */
            .dashview-panel-button:focus,
            .dashview-faux-button:focus {
                background: var(--tp-button-background-color-focus);
                outline: none;
            }

            /* Keyboard focus state for tabs and title bar. */
            .dashview-panel-tab:focus,
            .dashview-panel-toggle:focus {
                background: var(--tp-container-background-color-focus);
                outline: none;
            }

            /* Mouse-down state for regular command buttons. */
            .dashview-panel-button:active,
            .dashview-faux-button:active {
                background: var(--tp-button-background-color-active);
            }
"""


def _button(title, className="dashview-panel-button", **props):
    return html.Button(title, className=className, **props)


def _faux_button(title):
    return html.Button(title, className="dashview-faux-button", type="button")


def _control(label, value=""):
    return html.Div(
        [
            html.Span(label, className="dashview-control-label"),
            html.Span(value, className="dashview-control-value"),
        ],
        className="dashview-control-row",
    )


def _tree_select(tree_name):
    return html.Div(
        [
            html.Div(
                [
                    html.Span("tree", className="dashview-control-label"),
                    html.Button(
                        tree_name,
                        id="tree-toggle",
                        className="dashview-tree-current",
                        type="button",
                    ),
                ],
                className="dashview-tree-row",
            ),
            html.Div(
                [
                    html.Button(
                        tree_name,
                        id="tree-option-current",
                        className="dashview-tree-option is-selected",
                        type="button",
                    )
                ],
                id="tree-options",
                className="dashview-tree-options",
                style={"display": "none"},
            ),
        ],
        className="dashview-tree-select",
    )


def _folder(title, children=None, open=False):
    class_name = "dashview-folder is-open" if open else "dashview-folder"
    return html.Div(
        [
            html.Div(title, className="dashview-folder-title"),
            html.Div(children or [], className="dashview-folder-body"),
        ],
        className=class_name,
    )


def _page(title, children, page_id=None, visible=False):
    page_children = []
    if title:
        page_children.append(html.Div(title, className="dashview-panel-page-title"))
    page_children.extend(children)

    return html.Div(
        page_children,
        id=page_id,
        className="dashview-panel-page",
        style={"display": "flex" if visible else "none"},
    )


def _main_page(tree_name):
    return _page(
        "",
        [
            _tree_select(tree_name),
            html.Div(
                [
                    _button(
                        "download",
                        id="download-toggle",
                        className="dashview-panel-button dashview-download-toggle",
                    ),
                    html.Div(
                        [
                            _button(
                                "newick",
                                id="download-newick-button",
                                className="dashview-panel-button dashview-download-option",
                            ),
                            _button(
                                "svg",
                                id="download-svg-button",
                                className="dashview-panel-button dashview-download-option",
                            ),
                            _button(
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
            _faux_button("upload"),
            _control("shape", "rectangular"),
            _control("node height min", ""),
            _control("content height min", ""),
            _folder("layouts"),
            _folder(
                "extra labels",
                [
                    _folder(
                        "properties",
                        [
                            _control("properties", ""),
                            _faux_button("add property"),
                        ],
                        open=True,
                    ),
                    _faux_button("add expression"),
                ],
            ),
            _control("select text", "false"),
            _control("smart zoom", "true"),
            _faux_button("share view"),
            _faux_button("fullscreen"),
            _faux_button("help"),
        ],
        page_id="control-panel-page-main",
        visible=True,
    )


def _selections_page():
    return _page(
        "Selections",
        [
            _folder("manually collapsed"),
            _folder("tags"),
            _folder("searches", [_faux_button("new search")], open=True),
        ],
        page_id="control-panel-page-selections",
    )


def _advanced_page():
    return _page(
        "Advanced",
        [
            _control("subtree", ""),
            _folder(
                "sort",
                [
                    _control("key", ""),
                    _control("reverse", "false"),
                    _faux_button("apply"),
                ],
            ),
            _folder(
                "circular",
                [
                    _control("radius", ""),
                    _control("angle start", ""),
                    _control("angle end", ""),
                ],
            ),
            _folder(
                "info",
                [
                    _folder(
                        "nodes",
                        [
                            _control("visible", ""),
                            _control("total", ""),
                            _control("leaves", ""),
                        ],
                        open=True,
                    ),
                    _folder(
                        "pointer position",
                        [
                            _control("x", ""),
                            _control("y", ""),
                        ],
                        open=True,
                    ),
                    _faux_button("show details"),
                ],
            ),
            _folder(
                "viewport",
                [
                    _faux_button("reset view"),
                    _folder("aligned bar", [_control("position", "")]),
                ],
            ),
            _folder(
                "zoom",
                [
                    _control("sensitivity", ""),
                    _control("smart zoom", "true"),
                ],
            ),
            _folder(
                "tree style",
                [
                    _faux_button("use original style"),
                    _folder(
                        "node",
                        [
                            _folder(
                                "box",
                                [
                                    _control("opacity", ""),
                                    _control("color", ""),
                                ],
                                open=True,
                            ),
                            _folder(
                                "dot",
                                [
                                    _control("shape", ""),
                                    _control("radius", ""),
                                    _control("opacity", ""),
                                    _control("color", ""),
                                ],
                                open=True,
                            ),
                        ],
                    ),
                    _folder(
                        "collapsed",
                        [
                            _control("shape", ""),
                            _control("opacity", ""),
                            _control("color", ""),
                            _control("width", ""),
                        ],
                    ),
                    _folder(
                        "lines",
                        [
                            _folder(
                                "hz (horizontal/length)",
                                [
                                    _control("color", ""),
                                    _control("width", ""),
                                ],
                                open=True,
                            ),
                            _folder(
                                "vt (vertical/children)",
                                [
                                    _control("color", ""),
                                    _control("width", ""),
                                    _control("pattern", ""),
                                ],
                                open=True,
                            ),
                        ],
                    ),
                    _folder("text", [_control("automatic size", "true")]),
                    _folder(
                        "sequence",
                        [
                            _control("render", "auto"),
                            _control("padding", ""),
                        ],
                    ),
                    _folder("legend", [_control("show legend", "false")]),
                ],
            ),
            _folder(
                "minimap",
                [
                    _control("width", ""),
                    _control("height", ""),
                    _control("show", "false"),
                ],
            ),
        ],
        page_id="control-panel-page-advanced",
    )


def make_control_panel(tree_name="current tree"):
    """Return the floating control panel used by the Dash tree view."""
    return html.Div(
        [
            html.Button(
                "Control panel",
                id="control-panel-toggle",
                className="dashview-panel-toggle",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Button(
                                "Main",
                                id="control-panel-tab-main",
                                className="dashview-panel-tab is-active",
                            ),
                            html.Button(
                                "Selections",
                                id="control-panel-tab-selections",
                                className="dashview-panel-tab",
                            ),
                            html.Button(
                                "Advanced",
                                id="control-panel-tab-advanced",
                                className="dashview-panel-tab",
                            ),
                        ],
                        className="dashview-panel-tabs",
                    ),
                    _main_page(tree_name),
                    _selections_page(),
                    _advanced_page(),
                ],
                id="control-panel-body",
                className="dashview-panel-body",
                style={"display": "none"},
            ),
        ],
        id="control-panel",
        className="dashview-control-panel is-collapsed",
    )
