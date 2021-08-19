from flaskr import app
from flaskr.db.seeds import init_db_with_seeds

@app.cli.command("init_db")
def init_db():
    """
    Initialize DB with seed data.
    """

    init_db_with_seeds()
