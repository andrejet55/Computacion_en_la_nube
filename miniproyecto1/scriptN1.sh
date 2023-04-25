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

sudo npm install -g consul
sudo npm install -g express

echo "Configurando el consul agent"
sleep 15
consul agent \
  -server \
  -bootstrap-expect=1 \
  -data-dir=/tmp/consul \
  -node=agent-one \
  -bind=192.168.100.2 \
  -enable-script-checks=true \
  -config-dir=/etc/consul.d \
  -ui \
  -client=0.0.0.0 > /dev/null 2>&1 &

sleep 5
consul join 192.168.100.5
sleep 5
consul join 192.168.100.4

echo "Instalando HAProxy"
sudo apt update && sudo apt upgrade
sudo apt -y install haproxy
sleep 5
sudo systemctl enable haproxy

echo "Configurando haproxy.cfg"
sudo cp /vagrant/haproxy.cfg  /etc/haproxy/

sudo cp /vagrant/errorweb.http /etc/haproxy/errors
sleep 5

echo "Inicializando haproxy"
sudo systemctl start haproxy

sudo systemctl restart haproxy