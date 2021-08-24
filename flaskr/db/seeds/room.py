import os


def load_csv_data(csv_file):
    import csv

    with open(csv_file) as f:
        reader = csv.reader(f)
        csv_data = [row for row in reader]

    rooms = [(name, int(room_id)) for name, room_id in csv_data]

    return rooms


csv_file = "flaskr/db/seeds/csv/rooms.csv"

if os.path.exists(csv_file):
    rooms = load_csv_data(csv_file)
else:
    rooms = [
            ("ルーム1", 2),
            ("ルーム2", 2),
            ("ルーム3", 2),
            ("ルーム4", 2),
            ("ルーム5", 3),
            ("ルーム6", 3),
            ("ルーム7", 4),
            ("ルーム8", 4),
            ]
