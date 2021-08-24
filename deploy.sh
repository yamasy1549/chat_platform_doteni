./build_docker_image.sh

docker context use myecscontext

# ecs-cli up --capability-iam --instance-type c1.xlarge --force --keypair chat_platform_doteni
ecs-cli compose service up
ecs-cli compose service ps

docker context use default

# ssh -i ~/Downloads/chat_platform_doteni.pem ec2-user@18.183.79.200
