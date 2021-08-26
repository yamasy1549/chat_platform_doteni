import os


def load_csv_data(csv_file):
    import csv

    with open(csv_file) as f:
        reader = csv.reader(f)
        csv_data = [row for row in reader]

    users = [(name, int(role), password) for name, role, password in csv_data]

    return users


csv_file = "flaskr/db/seeds/csv/users.csv"

if os.path.exists(csv_file):
    users = load_csv_data(csv_file)
else:
    users = [
            ("test1", 1, "test1"),
            ("test2", 2, "test2"),
            ("test3", 2, "test3"),
            ("test4", 2, "test4"),
            ]
