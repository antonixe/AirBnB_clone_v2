#!/usr/bin/python3
"""a Fabric script (based on the file 2-do_deploy_web_static.py) that\
        creates and distributes an archive to your web servers, using\
        the function deploy"""

from fabric.api import run, env, put
import os.path
from fabric.api import local
from datetime import datetime

env.hosts = ['100.26.154.245', '54.144.221.234']
env.key_filename = '~/.ssh/school'
env.user = 'ubuntu'


def do_pack():
    """Compress the contents of web_static folder and return\
            the path of the archive"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    pathfile = "versions/web_static_{}.tgz".format(timestamp)

    try:
        local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(pathfile))
        return pathfile
    except Exception as e:
        return None


def do_deploy(archive_path):
    """Generate the .tgz archive from the contents of web_static folder"""

    if not os.path.isfile(archive_path):
        return False

    # Get the name of the compressed file and remove the file extension
    compressed_file = archive_path.split("/")[-1]
    no_extension = compressed_file.split(".")[0]

    try:
        # Define the remote path and symlink to be used for deployment
        remote_path = "/data/web_static/releases/{}/".format(no_extension)
        sym_link = "/data/web_static/current"

        # Upload the compressed file to the server
        put(archive_path, "/tmp/")

        """ Create the directory for the release and extract the compressed\
                file into it"""
        run("sudo mkdir -p {}".format(remote_path))
        run("sudo tar -xvzf /tmp/{} -C {}".format(
            compressed_file, remote_path))

        """Clean up the compressed file and move the web files to the\
                release directory"""
        run("sudo rm /tmp/{}".format(compressed_file))
        run("sudo mv {}/web_static/* {}".format(remote_path, remote_path))
        run("sudo rm -rf {}/web_static".format(remote_path))

        # Update the symlink to point to the new release directory
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -sf {} {}".format(remote_path, sym_link))

        # Return success if the deployment was successful
        return True
    except Exception as e:

        # If an exception occurred during deployment, return failure
        return False


def deploy():
    """call do_pack() and do_deploy"""
    file_path = do_pack()
    if file_path is None:
        return False
    return do_deploy(file_path)
