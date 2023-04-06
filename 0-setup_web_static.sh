#!/usr/bin/env bash
#  a Bash script that sets up your web servers for the deployment of web_static
# install nginx if not installed
if [ "$(dpkg-query -W -f='${Status}' nginx 2>/dev/null | grep -c 'installed')" -eq 0 ];
then
        #install nginx
        echo "Nginx is not installed ...installing nginx"
        sudo apt update
        sudo apt install nginx
else
        echo "Nginx is already installed"
fi

# Create the folder /data/ if it doesn’t already exist
if [ ! -d '/data/' ]; then
        sudo mkdir /data
fi

# Create the folder /data/web_static/ if it doesn’t already exist
if [ ! -d '/data/web_static/' ]; then
        sudo mkdir /data/web_static/
fi

# Create the folder /data/web_static/releases/ if it doesn’t already exist
if [ ! -d '/data/web_static/releases/' ]; then
        sudo mkdir /data/web_static/releases/
fi

# Create the folder /data/web_static/shared/ if it doesn’t already exist
if [ ! -d '/data/web_static/shared/' ]; then
        sudo mkdir /data/web_static/shared/
fi

# Create the folder /data/web_static/releases/test/ if it doesn’t already exist
if [ ! -d '/data/web_static/releases/test/' ]; then
        sudo mkdir /data/web_static/releases/test/
fi

# Create a fake HTML file /data/web_static/releases/test/index.html (with simple content, to test your Nginx configuration)
sudo tee /data/web_static/releases/test/index.html >/dev/null <<EOF
<!DOCTYPE html>
    <head>
    </head>
    <body>
        Holberton School
    </body>
</html>
EOF

# Create a symbolic link /data/web_static/current linked to the /data/web_static/releases/test/ folder. If the symbolic link already exists, it should be deleted and recreated every time the script is ran.
if [ -L '/data/web_static/current' ]; then
        sudo rm /data/web_static/current
fi
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user AND group (you can assume this user and group exist). This should be recursive; everything inside should be created/owned by this user/group.
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static (ex: https://mydomainname.tech/hbnb_static
sudo sed -i '/server_name _;/a \ \tlocation /hbnb_static {\n\t\talias /data/web_static/current;\n\t}\n' /etc/nginx/sites-available/default

sudo nginx -t

if sudo nginx -t >/dev/null 2>&1; then
        sudo service nginx restart
fi
