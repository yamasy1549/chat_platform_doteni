from flask import Blueprint, redirect, url_for


bp = Blueprint("index", __name__)


@bp.route("/", methods=["GET"])
def root():
    """
    [GET] /

    ルート
    """

    return redirect(url_for("entries.index"))
