from flaskr.models import Entry


seeds = [
        ("対話1", "あああ\nいいい\nううううう"),
        ("対話2", "aaa\nbbb\nccccc"),
        ]

entries = [Entry(title=d[0], text=d[1]) for d in seeds]
