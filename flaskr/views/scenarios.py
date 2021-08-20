from flask import Blueprint, current_app, render_template, redirect, url_for, flash, request
from flaskr.core import db
from flaskr.models.scenario import Scenario
from flaskr.views import admin_required


bp = Blueprint("scenarios", __name__, url_prefix="/scenarios")


@bp.route("/")
@admin_required
def index():
    """
    [GET] /scenarios

    シナリオの一覧
    """

    scenarios = Scenario.query.order_by(Scenario.id.desc()).all()
    return render_template("scenarios/index.html", scenarios=scenarios)

@bp.route("/<int:scenario_id>/edit", methods=["GET", "POST"])
@admin_required
def edit(scenario_id):
    """
    [GET] /scenarios/:scenario_id/edit
    [POST] /scenarios/:scenario_id/edit

    シナリオの編集
    """

    scenario = Scenario.query.get(scenario_id)
    if scenario is None:
        abort(404)
    if request.method == "POST":
        scenario.title = request.form["title"]
        scenario.text = request.form["text"]
        db.session.add(scenario)
        db.session.commit()
        return redirect(url_for("scenarios.index"))
    return render_template("scenarios/edit.html", scenario=scenario)

@bp.route("/create", methods=["GET", "POST"])
@admin_required
def create():
    """
    [GET] /scenarios/create
    [POST] /scenarios/create

    シナリオの新規作成
    """

    if request.method == "POST":
        scenario = Scenario(
                title=request.form["title"],
                text=request.form["text"]
                )
        db.session.add(scenario)
        db.session.commit()
        flash("新しいシナリオを作成しました")
        return redirect(url_for("scenarios.index"))

    return render_template("scenarios/edit.html")

@bp.route("/<int:scenario_id>/delete", methods=["POST"])
@admin_required
def delete(scenario_id):
    """
    [POST] /scenarios/:scenario_id/delete

    シナリオの削除
    """

    scenario = Scenario.query.get(scenario_id)
    if scenario is None:
        response = jsonify({"status": "Not Found"})
        response.status_code = 404
        return response
    db.session.delete(scenario)
    db.session.commit()
    return redirect(url_for("scenarios.index"))
