#!/usr/bin/python3
"""
A script to deploy an archive file to a remote server and decompress it.
"""
import os.path
from fabric.api import env, put, run

env.hosts = ['54.144.221.234', '100.26.154.245']
env.key_filename = '~/.ssh/school'
env.user = 'ubuntu'


def deploy_archive(archive_path):
    """
    Deploy an archive file to a remote server and decompress it.
    """
    if not os.path.isfile(archive_path):
        return False

    filename = os.path.basename(archive_path)
    filename_no_ext = os.path.splitext(filename)[0]
    remote_dir = "/data/web_static/releases/{}/".format(filename_no_ext)
    current_dir = "/data/web_static/current"

    try:
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(remote_dir))
        run("sudo tar -xzf /tmp/{} -C {}".format(filename, remote_dir))
        run("sudo rm /tmp/{}".format(filename))
        run("sudo mv {}web_static/* {}".format(remote_dir, remote_dir))
        run("sudo rm -rf {}web_static/".format(remote_dir))
        run("sudo rm -rf {}".format(current_dir))
        run("sudo ln -s {} {}".format(remote_dir, current_dir))
        return True
    except Exception:
        return False
