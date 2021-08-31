docker context use default

docker-compose -f docker-compose.yml -f docker-compose.development.yml up
# docker-compose -f docker-compose.yml -f docker-compose.production.yml exec uwsgi flask init_db_with_seeds
