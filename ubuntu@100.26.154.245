#!/usr/bin/env bash
# Install Nginx if not already installed
command -v nginx > /dev/null || sudo apt-get -y update && sudo apt-get -y install nginx

# Create necessary directories and files
sudo mkdir -p /data/web_static/releases/test/ /data/web_static/shared/
echo "Holberton School" | sudo tee /data/web_static/releases/test/index.html

# Create symbolic link and give ownership to ubuntu user and group
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve content from /data/web_static/current/ to hbnb_static
sudo sed -i '/^\tserver_name localhost;$/a\\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default
sudo service nginx restart
