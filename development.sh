docker context use default

# Dockerコンテナ (uwsgi, nginx) を終了するには
docker-compose -f docker-compose.yml -f docker-compose.development.yml down

# Dockerコンテナ (uwsgi, nginx) を起動するには
docker-compose -f docker-compose.yml -f docker-compose.development.yml up

# Dockerコンテナ (uwsgi, nginx) を起動し、そのプロセスをデーモン化するには
# docker-compose -f docker-compose.yml -f docker-compose.development.yml up -d

# 起動中のDockerコンテナ (uwsgi) の中に入るには
# docker-compose -f docker-compose.yml -f docker-compose.development.yml exec --rm -it uwsgi /bin/bash

# 起動中のDockerコンテナ (uwsgi) でコマンドを実行 (flask init_db_with_seeds) するには
# docker-compose -f docker-compose.yml -f docker-compose.development.yml exec --rm -it uwsgi flask init_db_with_seeds

# Dockerコンテナ (uwsgi, nginx) を停止するには
# docker-compose -f docker-compose.yml -f docker-compose.development.yml down
