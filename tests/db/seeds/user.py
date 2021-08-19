from flaskr.models import User


seeds = [
        ("test1", "test1", "test1"),
        ("test2", "test2", "test2"),
        ]

users = [User(name=d[0], email=d[1], password=d[2]) for d in seeds]
