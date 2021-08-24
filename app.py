from flaskr import app
from flaskr.db import init_db as _init_db, init_db_with_seeds as _init_db_with_seeds


@app.cli.command("init_db")
def init_db():
    """
    Initialize DB.
    """

    _init_db()

@app.cli.command("init_db_with_seeds")
def init_db_with_seeds():
    """
    Initialize DB with seed data.
    """

    _init_db_with_seeds()


if __name__ == "__main__":
    app.run()
