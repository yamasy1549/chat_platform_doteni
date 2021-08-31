.
├── README.md
├── app.py
├── config_nginx
│   ├── Dockerfile.development
│   ├── Dockerfile.production
│   └── nginx.conf
├── config_uwsgi
│   ├── Dockerfile.development
│   ├── Dockerfile.production
│   ├── uwsgi.ini
│   └── uwsgi_init.sh
├── deploy.sh
├── development.sh
├── docker-compose.development.yml
├── docker-compose.production.yml
├── docker-compose.yml
├── flaskr
│   ├── __init__.py
│   ├── config.py
│   ├── core.py
│   ├── db
│   │   ├── __init__.py
│   │   └── seeds
│   │       ├── __init__.py
│   │       ├── csv
│   │       │   ├── room_scenarios.csv
│   │       │   ├── rooms.csv
│   │       │   ├── scenarios.csv
│   │       │   └── users.csv
│   │       ├── message.py
│   │       ├── room.py
│   │       ├── room_scenario.py
│   │       ├── scenario.py
│   │       └── user.py
│   ├── factory.py
│   ├── flaskr.db
│   ├── logs.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── error.py
│   │   ├── message.py
│   │   ├── room.py
│   │   ├── room_scenario.py
│   │   ├── room_user.py
│   │   ├── scenario.py
│   │   └── user.py
│   ├── static
│   │   ├── reset.css
│   │   └── style.css
│   ├── templates
│   │   ├── auth
│   │   │   └── login.html
│   │   ├── layout.html
│   │   ├── rooms
│   │   │   ├── edit.html
│   │   │   ├── index.html
│   │   │   └── show.html
│   │   ├── scenarios
│   │   │   ├── edit.html
│   │   │   └── index.html
│   │   └── users
│   │       ├── edit.html
│   │       └── index.html
│   └── views
│       ├── __init__.py
│       ├── auth.py
│       ├── index.py
│       ├── rooms.py
│       ├── scenarios.py
│       ├── socketio.py
│       └── users.py
├── logs
│   ├── debug.log
│   ├── debug.log.1
│   ├── debug.log.10
│   ├── debug.log.2
│   ├── debug.log.3
│   ├── debug.log.4
│   ├── debug.log.5
│   ├── debug.log.6
│   ├── debug.log.7
│   ├── debug.log.8
│   ├── debug.log.9
│   └── error.log
├── nginx.conf
├── requirements.txt
└── tests
    ├── __init__.py
    ├── conftest.py
    ├── db
    │   └── seeds
    │       ├── room.py
    │       ├── room_scenario.py
    │       ├── scenario.py
    │       └── user.py
    └── views
        ├── __init__.py
        ├── test_auth.py
        ├── test_index.py
        ├── test_required.py
        ├── test_rooms.py
        ├── test_scenarios.py
        └── test_users.py

20 directories, 85 files

