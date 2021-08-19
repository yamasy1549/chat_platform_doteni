from flaskr.models import Entry


seeds = [
        ("entry1", "あああ\nいいい\nううううう"),
        ("entry2", "aaa\nbbb\nccccc"),
        ]

entries = [Entry(title=d[0], text=d[1]) for d in seeds]
