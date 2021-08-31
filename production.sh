#
# Docker image のビルド
#
docker context use default

aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin 154234079813.dkr.ecr.ap-northeast-1.amazonaws.com

docker build -t chat_platform_doteni_uwsgi:latest -f ./config_uwsgi/Dockerfile.production .
docker tag chat_platform_doteni_uwsgi:latest 154234079813.dkr.ecr.ap-northeast-1.amazonaws.com/chat_platform_doteni_uwsgi:latest
docker push 154234079813.dkr.ecr.ap-northeast-1.amazonaws.com/chat_platform_doteni_uwsgi:latest

docker build -t chat_platform_doteni_nginx:latest -f ./config_nginx/Dockerfile.production .
docker tag chat_platform_doteni_nginx:latest 154234079813.dkr.ecr.ap-northeast-1.amazonaws.com/chat_platform_doteni_nginx:latest
docker push 154234079813.dkr.ecr.ap-northeast-1.amazonaws.com/chat_platform_doteni_nginx:latest

# docker-compose push

#
# ECSへのデプロイ
#
docker context use myecscontext

# ecs-cli up --capability-iam --instance-type c1.xlarge --force --keypair chat_platform_doteni
ecs-cli compose -f docker-compose.yml -f docker-compose.production.yml service up
ecs-cli compose -f docker-compose.yml -f docker-compose.production.yml service ps

docker context use default

# ssh -i ~/Downloads/chat_platform_doteni.pem ec2-user@18.183.79.200
