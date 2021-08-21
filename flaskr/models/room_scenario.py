from flaskr.core import db


room_scenarios = db.Table("room_scenarios",
        db.Column("room_id",     db.Integer, db.ForeignKey("rooms.id"),     primary_key=True),
        db.Column("scenario_id", db.Integer, db.ForeignKey("scenarios.id"), primary_key=True),
        )
