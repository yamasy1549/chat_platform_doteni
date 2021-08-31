# （初回のみ）ECSでクラスタを作成するには
# ecs-cli up --capability-iam --instance-type t2.medium --keypair キーペア名


# DockerイメージをビルドしてECRへアップロード
docker context use default
aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin 154234079813.dkr.ecr.ap-northeast-1.amazonaws.com

docker build -t chat_platform_doteni_uwsgi:latest -f ./config_uwsgi/Dockerfile.production .
docker build -t chat_platform_doteni_nginx:latest -f ./config_nginx/Dockerfile.production .
docker tag chat_platform_doteni_uwsgi:latest 154234079813.dkr.ecr.ap-northeast-1.amazonaws.com/chat_platform_doteni_uwsgi:latest
docker tag chat_platform_doteni_nginx:latest 154234079813.dkr.ecr.ap-northeast-1.amazonaws.com/chat_platform_doteni_nginx:latest
docker-compose -f docker-compose.yml -f docker-compose.production.yml push


# ECSへデプロイ
docker context use myecscontext
ecs-cli compose -f docker-compose.yml -f docker-compose.production.yml service down
sleep 60
ecs-cli compose -f docker-compose.yml -f docker-compose.production.yml service up
ecs-cli compose -f docker-compose.yml -f docker-compose.production.yml service ps
docker context use default

# 起動中のサーバの中に入るには
# ssh -i chat_platform_doteni.pem ec2-user@XX.XX.XX.XX

# 起動中のサーバの中で、起動中のDockerコンテナの中に入るには
# docker ps   # コンテナのIDを確認
# docker exec --it コンテナのID /bin/bash
