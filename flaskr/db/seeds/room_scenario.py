import os


def load_csv_data(csv_file):
    import csv

    with open(csv_file) as f:
        reader = csv.reader(f)
        csv_data = [row for row in reader]

    room_scenarios = [(int(room_id), int(scenario_id)) for room_id, scenario_id in csv_data]

    return room_scenarios


csv_file = "flaskr/db/seeds/csv/room_scenarios.csv"

if os.path.exists(csv_file):
    room_scenarios = load_csv_data(csv_file)
else:
    room_scenarios = [
            (1, 1),
            (1, 2),
            (2, 1),
            (2, 2),
            (3, 3),
            (3, 4),
            (4, 3),
            (4, 4),
            ]
