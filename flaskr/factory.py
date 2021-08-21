from flask import Flask
from flask_socketio import SocketIO
from flaskr.core import db
from flaskr import logs, views


socketio = SocketIO()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_object("flaskr.config")
    else:
        app.config.from_mapping(test_config)

    db.init_app(app)
    logs.init_app(app)
    views.init_app(app)

    socketio.init_app(app)
    socketio.run(app=app, host="localhost", port="5001")

    return app
