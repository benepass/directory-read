#!/bin/bash

# Run me as root!

curl -fsSL https://tailscale.com/install.sh | sh;
yum check-update;
yum install docker;
curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose;
chmod +x /usr/local/bin/docker-compose;
service docker start;
usermod -a -G docker ssm-user;
curl 'https://raw.githubusercontent.com/mage-ai/docker/master/docker-compose.yml' > /home/ssm-user/docker-compose.yml;
chown ssm-user /home/ssm-user/docker-compose.yml;
