from dash import dcc, html


UPLOAD_STYLE = r"""
            .dashview-upload-page {
                display: none;
                position: fixed;
                inset: 0;
                z-index: 1000;
                min-height: 100vh;
                overflow: auto;
                flex-direction: column;
                box-sizing: border-box;
                background: white;
                color: black;
                font-family: serif;
            }

            .dashview-upload-centered {
                width: calc(100% - 2em);
                max-width: 800px;
                margin: 0 auto;
                padding: 0 1em;
                box-sizing: border-box;
            }

            .dashview-upload-page h1 {
                color: #333;
                border-bottom: 3px solid #00b894;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
            }

            .dashview-upload-page .upload-spacing {
                margin: 0.5rem 0.2rem;
            }

            .dashview-upload-page fieldset {
                display: inline-block;
                border: 2px solid #DDD;
                border-radius: 4px;
            }

            .dashview-upload-page button {
                padding: 12px 24px;
                background-color: #0ea5e9;
                color: white;
                border: 0;
                border-radius: 6px;
                font-size: 1rem;
                font-weight: 500;
                cursor: pointer;
                transition: transform 0.2s, box-shadow 0.2s;
            }

            .dashview-upload-page button:hover {
                background-color: #0284c7;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }

            .dashview-upload-page button:active {
                transform: translateY(0);
                box-shadow: none;
            }

            .dashview-upload-page input,
            .dashview-upload-page label,
            .dashview-upload-page textarea {
                margin: 0.4rem 0;
            }

            .dashview-upload-file {
                display: inline-block;
                margin-left: 0.35rem;
                vertical-align: middle;
            }

            .dashview-upload-file > div {
                padding: 2px 6px;
                border: 1px solid #767676;
                border-radius: 2px;
                background: #efefef;
                cursor: pointer;
                font: 13.3333px Arial;
            }

            .dashview-upload-status {
                min-height: 1.2em;
                color: #b42318;
            }

            .dashview-upload-footer {
                flex: 1;
                margin: 2em 0 0;
                padding: 2em 0 0;
                background-color: #EEE;
                font-size: 0.9em;
            }

            .dashview-upload-page kbd {
                display: inline-block;
                padding: 2px 4px;
                border: 1px solid #b4b4b4;
                border-radius: 3px;
                background-color: #eee;
                box-shadow: 0 1px 1px rgba(0, 0, 0, .2),
                            0 2px 0 0 rgba(255, 255, 255, .7) inset;
                color: #333;
                font-size: .85em;
                font-weight: 700;
                line-height: 1;
                white-space: nowrap;
            }
"""


def make_upload_page():
    """Build the Dash equivalent of SmartView's upload.html page."""
    return html.Div(
        [
            html.Div(
                [
                    html.H1("ETE Tree Explorer"),
                    html.P([
                        "This is a tool for exploring trees. It is mainly used to explore ",
                        html.A("phylogenetic trees", href="https://en.wikipedia.org/wiki/Phylogenetic_tree"),
                        ", but it can be used for any kind of tree.",
                    ]),
                    html.P([
                        "You can ",
                        html.A("explore the pre-loaded trees", href="#", id="upload-back-link"),
                        ", or add your own trees for exploration by uploading them from this page.",
                    ]),
                    html.P([
                        "The tree can be written in the ",
                        html.A("newick format", href="https://en.wikipedia.org/wiki/Newick_format"),
                        " or a depth-indented listing (like the output of the ",
                        html.Code("tree"),
                        " program).",
                    ]),
                    html.P([
                        "When using the interactive gui for exploration, press ",
                        html.Kbd("F1"),
                        " or the help button in the viewer for instructions.",
                    ]),
                    html.Div(
                        [
                            html.Fieldset(
                                [
                                    html.Legend("Tree"),
                                    html.Div(
                                        [
                                            dcc.RadioItems(
                                                id="upload-source",
                                                options=[
                                                    {"label": "From string", "value": "string"},
                                                    {"label": "From file", "value": "file"},
                                                ],
                                                value=None,
                                            ),
                                            html.Span([
                                                "(",
                                                html.A(
                                                    "load an example",
                                                    href="#",
                                                    id="upload-load-example",
                                                ),
                                                ")",
                                            ]),
                                            dcc.Textarea(
                                                id="upload-string",
                                                rows=8,
                                                placeholder="Newick or indented representation of the tree",
                                                disabled=True,
                                                style={"width": "100%", "boxSizing": "border-box"},
                                            ),
                                            html.Div(
                                                [
                                                    html.Span("From file:"),
                                                    dcc.Upload(
                                                        html.Div("Choose File"),
                                                        id="upload-file",
                                                        className="dashview-upload-file",
                                                        multiple=False,
                                                        disabled=True,
                                                        accept=".tree,.newick,.nw,.tre,.nex,.nxs,.nexus,.txt,.gz,.bz2,.tgz,.tar,.zip",
                                                    ),
                                                    html.Span(id="upload-filename"),
                                                ],
                                                className="upload-spacing",
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                            html.Fieldset(
                                [
                                    html.Legend("How to parse"),
                                    dcc.RadioItems(
                                        id="upload-parser",
                                        options=[
                                            {"label": "((name:dist)name:dist); (newick with internal node name)", "value": "name"},
                                            {"label": "((name:dist)support:dist); (newick with internal node support)", "value": "support"},
                                            {"label": "Depth-indented listing", "value": "indent"},
                                        ],
                                        value="name",
                                    ),
                                ],
                                className="upload-spacing",
                            ),
                            dcc.Checklist(
                                id="upload-add-name",
                                options=[{"label": "Add name", "value": "name"}],
                                value=[],
                            ),
                            html.Div(
                                [
                                    html.Label("Name (1 to 128 characters)", htmlFor="upload-name"),
                                    html.Br(),
                                    dcc.Input(
                                        id="upload-name",
                                        type="text",
                                        placeholder="Tree name",
                                        minLength=1,
                                        maxLength=128,
                                        size="20",
                                    ),
                                ],
                                id="upload-name-container",
                                style={"display": "none"},
                            ),
                            html.P(id="upload-status", className="dashview-upload-status"),
                            html.Button("Upload and explore tree", id="upload-submit", type="button"),
                        ],
                        className="upload-spacing",
                    ),
                ],
                className="dashview-upload-centered",
            ),
            html.Footer(html.Div(className="dashview-upload-centered"), className="dashview-upload-footer"),
        ],
        id="upload-page",
        className="dashview-upload-page",
        style={"display": "none"},
    )
