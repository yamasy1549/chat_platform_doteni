docker context use default

docker build --tag yamasy1549/chat_platform_doteni_nginx:latest -f Dockerfile.nginx .
docker push yamasy1549/chat_platform_doteni_nginx:latest

docker build --tag yamasy1549/chat_platform_doteni_uwsgi:latest -f Dockerfile.uwsgi .
docker push yamasy1549/chat_platform_doteni_uwsgi:latest
