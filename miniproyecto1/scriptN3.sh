#!/bin/bash

echo "Instalando net tools"
sudo apt-get -y install net-tools

echo "Instalando consul"
wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt -y install consul

echo "Instalando nodejs"
sudo apt -y install nodejs
node -v
sudo apt -y install npm
npm -v

sudo mkdir -p consulService/app

sudo cp /vagrant/consulService/app/index3.js consulService/app

cd consulService/app

sudo npm install consul
sudo npm install express


echo "Configurando el consul agent"
sleep 15
consul agent \
  -data-dir=/tmp/consul \
  -node=agent-three \
  -bind=192.168.100.4 \
  -enable-script-checks=true \
  -config-dir=/etc/consul.d > /dev/null 2>&1 &
sleep 5
node consulService/app/index3.js 3000 > /dev/null 2>&1 &
sleep 5
node consulService/app/index3.js 3001 > /dev/null 2>&1 &