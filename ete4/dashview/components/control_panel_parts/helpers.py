from dash import dcc, html


def button(title, className="dashview-panel-button", **props):
    return html.Button(title, className=className, **props)


def faux_button(title, **props):
    return html.Button(
        title,
        className="dashview-faux-button",
        type="button",
        **props,
    )


def control(label, value=""):
    return html.Div(
        [
            html.Span(label, className="dashview-control-label"),
            html.Span(value, className="dashview-control-value"),
        ],
        className="dashview-control-row",
    )


def number_control(label, value, component_id, minimum, maximum):
    return html.Div(
        [
            html.Label(label, htmlFor=component_id, className="dashview-control-label"),
            dcc.Input(
                id=component_id,
                className="dashview-control-value dashview-number-input",
                type="number",
                value=value,
                min=minimum,
                max=maximum,
                step=1,
                debounce=False,
            ),
        ],
        className="dashview-control-row dashview-number-control",
    )


def folder(title, children=None, open=False):
    class_name = "dashview-folder is-open" if open else "dashview-folder"
    return html.Div(
        [
            html.Div(title, className="dashview-folder-title"),
            html.Div(children or [], className="dashview-folder-body"),
        ],
        className=class_name,
    )


def page(title, children, page_id=None, visible=False):
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
