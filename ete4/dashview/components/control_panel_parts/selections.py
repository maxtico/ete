from .helpers import faux_button, folder, page


def selections_page():
    return page(
        "Selections",
        [
            folder("manually collapsed"),
            folder("tags"),
            folder("searches", [faux_button("new search")], open=True),
        ],
        page_id="control-panel-page-selections",
    )
