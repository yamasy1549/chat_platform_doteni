from flask import Flask
from flaskr import logs, views
from flaskr.core import db, socketio


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_object("flaskr.config")
    else:
        app.config.from_mapping(test_config)

    logs.init_app(app)
    views.init_app(app)
    db.init_app(app)
    socketio.init_app(app)

    return app
