#!/usr/bin/python3
"""a script to send an archive file to a remote server
and decompress it"""

from fabric.api import run, env, put
import os.path

env.hosts = ['100.26.154.245', '54.144.221.234']
env.key_filename = '~/.ssh/my_ssh_key'
env.user = 'ubuntu'

def deploy_code(archive_path):
    """a function to deploy code and decompress it"""
    
    # Check if the archive file exists and is not a directory
    if not os.path.isfile(archive_path) or os.path.isdir(archive_path):
        return False
    
    compressed_file = archive_path.split("/")[-1]
    no_extension = compressed_file.split(".")[0]
    
    try:
        remote_path = "/var/www/releases/{}/".format(no_extension)
        sym_link = "/var/www/current"
        
        # Upload the archive file to the remote server
        put(archive_path, "/tmp/")
        
        # Create the directory for the new release
        run("sudo mkdir -p {}".format(remote_path))
        
        # Extract the files from the archive
        run("sudo tar -xvzf /tmp/{} -C {}".format(compressed_file, remote_path))
        
        # Remove the archive file from the remote server
        run("sudo rm /tmp/{}".format(compressed_file))
        
        # Move the extracted files to the release directory
        run("sudo mv {}/web_static/* {}".format(remote_path, remote_path))
        
        # Remove the old web_static directory
        run("sudo rm -rf {}/web_static".format(remote_path))
        
        # Update the symbolic link to point to the new release
        run("sudo rm -rf {}".format(sym_link))
        run("sudo ln -sf {} {}".format(remote_path, sym_link))
        
        return True
    except Exception as e:
        return False

