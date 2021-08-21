from flask import Blueprint, current_app, render_template, redirect, url_for, flash, request
from flaskr.core import db
from flaskr.models import Entry
from flaskr.views import login_required, admin_required


bp = Blueprint("entries", __name__, url_prefix="/entries")


@bp.route("/")
@login_required
def index():
    """
    [GET] /entries

    エントリの一覧
    """

    entries = Entry.query.order_by(Entry.id.desc()).all()
    return render_template("entries/index.html", entries=entries)

@bp.route("/<int:entry_id>/edit", methods=["GET", "POST"])
@admin_required
def edit(entry_id):
    """
    [GET] /entries/:entry_id/edit
    [POST] /entries/:entry_id/edit

    エントリの編集
    """

    entry = Entry.query.get(entry_id)
    if entry is None:
        abort(404)
    if request.method == "POST":
        entry.title = request.form["title"]
        entry.text = request.form["text"]
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for("entries.index"))
    return render_template("entries/edit.html", entry=entry)

@bp.route("/create", methods=["GET", "POST"])
@admin_required
def create():
    """
    [GET] /entries/create
    [POST] /entries/create

    エントリの新規作成
    """

    if request.method == "POST":
        entry = Entry(
                title=request.form["title"],
                text=request.form["text"]
                )
        db.session.add(entry)
        db.session.commit()
        flash("新しいEntryを作成しました")
        return redirect(url_for("entries.index"))

    return render_template("entries/edit.html")

@bp.route("/<int:entry_id>/delete", methods=["POST"])
@admin_required
def delete(entry_id):
    """
    [POST] /entries/:entry_id/delete

    エントリの削除
    """

    entry = Entry.query.get(entry_id)
    if entry is None:
        response = jsonify({"status": "Not Found"})
        response.status_code = 404
        return response
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for("entries.index"))
