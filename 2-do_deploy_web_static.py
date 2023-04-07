#!/usr/bin/python3
"""a Fabric script (based on the file 1-pack_web_static.py) that\
        distributes an archive to your web servers, using the\
        function do_deploy"""

from fabric.api import run, env, put
import os.path

env.hosts = ['54.144.221.234', '100.26.154.245']
env.key_filename = '~/.ssh/school'
env.user = 'ubuntu'


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
