#!/usr/bin/env bash
# A script that installs and configs nginx
# The steps include
# install nginx, creates the repositories, symbolic link also give ownership to /data/,configuring nginx and restart it
sudo apt-get update
sudo apt-get install nginx -y
sudo mkdir -p /data/web_static/releases/test/ 
sudo mkdir -p /data/web_static/shared/
echo " Holberton School" | sudo tee /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/
sudo sed -i '38i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default
sudo service nginx start
