import base64
import bz2
import gzip
import hashlib
import io
import os
import tarfile
import time
import zipfile

from dash import Input, Output, State, callback_context, no_update
from ete4 import Tree, nexus


MAX_UPLOAD_BYTES = 30_000_000
MAX_EXTRACTED_BYTES = 100_000_000
DASHBOARD_VISIBLE = {
    "position": "fixed",
    "inset": 0,
    "display": "block",
}
DASHBOARD_HIDDEN = {
    "position": "fixed",
    "inset": 0,
    "display": "none",
}


def _trees_from_text(raw, default_name):
    text = raw.decode("utf8").strip()
    try:
        trees = nexus.get_trees(text)
        return list(trees.items())
    except nexus.NexusError:
        return [(default_name, text)]


def _trees_from_file(filename, raw):
    """Extract named Newick strings using SmartView's upload semantics."""
    filename_lower = filename.lower()
    extracted = []

    if filename_lower.endswith(".zip"):
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            for info in archive.infolist():
                if not info.is_dir():
                    extracted.append((info.filename, archive.read(info)))
    elif filename_lower.endswith((".tar", ".tar.gz", ".tgz")):
        mode = "r:gz" if filename_lower.endswith((".tar.gz", ".tgz")) else "r:"
        with tarfile.open(fileobj=io.BytesIO(raw), mode=mode) as archive:
            for member in archive.getmembers():
                if member.isfile():
                    stream = archive.extractfile(member)
                    if stream is not None:
                        extracted.append((member.name, stream.read()))
    elif filename_lower.endswith(".gz"):
        extracted.append((filename[:-3], gzip.decompress(raw)))
    elif filename_lower.endswith(".bz2"):
        extracted.append((filename[:-4], bz2.decompress(raw)))
    else:
        extracted.append((filename, raw))

    if sum(len(content) for _, content in extracted) > MAX_EXTRACTED_BYTES:
        raise ValueError("The extracted files are too large (maximum 100 MB)")

    trees = []
    for member_name, content in extracted:
        default_name = os.path.splitext(os.path.basename(member_name))[0]
        trees.extend(_trees_from_text(content, default_name))
    return trees


def _unique_name(name, existing):
    name = name.replace(",", "_")
    if name not in existing:
        return name
    index = 2
    while f"{name} ({index})" in existing:
        index += 1
    return f"{name} ({index})"


def register_upload_callbacks(app, trees):
    @app.callback(
        Output("upload-string", "disabled"),
        Output("upload-file", "disabled"),
        Input("upload-source", "value"),
    )
    def choose_upload_source(source):
        return source != "string", source != "file"

    @app.callback(
        Output("upload-name-container", "style"),
        Input("upload-add-name", "value"),
    )
    def toggle_upload_name(values):
        return {"display": "block" if "name" in (values or []) else "none"}

    @app.callback(
        Output("upload-source", "value"),
        Output("upload-string", "value"),
        Input("upload-load-example", "n_clicks"),
        prevent_initial_call=True,
    )
    def load_example(n_clicks):
        if not n_clicks:
            return no_update, no_update
        return "string", "((A:1,B:1):1,(C:1,D:1):1);"

    @app.callback(
        Output("upload-filename", "children"),
        Input("upload-file", "filename"),
    )
    def show_filename(filename):
        return f" {filename}" if filename else " No file chosen"

    @app.callback(
        Output("upload-page", "style"),
        Output("dashboard-page", "style"),
        Output("tree-names", "data"),
        Output("upload-result", "data"),
        Output("upload-status", "children"),
        Input("upload-open", "n_clicks"),
        Input("upload-back-link", "n_clicks"),
        Input("upload-submit", "n_clicks"),
        State("upload-source", "value"),
        State("upload-string", "value"),
        State("upload-file", "contents"),
        State("upload-file", "filename"),
        State("upload-parser", "value"),
        State("upload-add-name", "value"),
        State("upload-name", "value"),
        prevent_initial_call=True,
    )
    def upload_tree(
        open_clicks,
        back_clicks,
        submit_clicks,
        source,
        tree_text,
        file_contents,
        filename,
        parser,
        add_name,
        supplied_name,
    ):
        triggered_id = callback_context.triggered_id
        if triggered_id == "upload-open":
            return {"display": "flex"}, DASHBOARD_HIDDEN, no_update, no_update, ""
        if triggered_id == "upload-back-link":
            return {"display": "none"}, DASHBOARD_VISIBLE, no_update, no_update, ""

        try:
            if source not in {"string", "file"}:
                raise ValueError("You need to supply a string or select a file")
            if "name" in (add_name or []) and not (supplied_name or "").strip():
                raise ValueError("Missing name")

            if source == "string":
                if not (tree_text or "").strip():
                    raise ValueError("Missing tree string")
                default_name = (
                    supplied_name.strip()
                    if "name" in (add_name or [])
                    else hashlib.sha1(str(time.time_ns()).encode()).hexdigest()[:12]
                )
                candidates = [(default_name, tree_text.strip())]
            else:
                if not file_contents or not filename:
                    raise ValueError("Missing file")
                _, encoded = file_contents.split(",", 1)
                raw = base64.b64decode(encoded, validate=True)
                if len(raw) >= MAX_UPLOAD_BYTES:
                    raise ValueError("Sorry, the file is too big (the maximum is 30 MB)")
                candidates = _trees_from_file(filename, raw)

            staged = {}
            for candidate_name, newick_text in candidates:
                name = _unique_name(candidate_name, {**trees, **staged})
                staged[name] = Tree(newick_text, parser=parser or "name")

            if not staged:
                raise ValueError("Could not find any tree in file")

            trees.update(staged)
            added = list(staged)
            result = {"name": added[0], "nonce": time.time_ns()}
            return (
                {"display": "none"},
                DASHBOARD_VISIBLE,
                list(trees),
                result,
                "",
            )
        except Exception as error:
            return (
                {"display": "flex"},
                DASHBOARD_HIDDEN,
                no_update,
                no_update,
                str(error),
            )
