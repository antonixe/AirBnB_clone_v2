#!/usr/bin/env python3
"""
Fabric script that creates and distributes an archive to your web servers
"""
from datetime import datetime
from fabric.api import env, put, run

env.hosts = ['54.144.221.234', '100.26.154.245']
env.user = 'ubuntu'
env.key_filename = ['~/.ssh/school']


def do_pack():
    """
    Compresses files from web_static folder
    """
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        local("mkdir -p versions")
        archive_path = "versions/web_static_{}.tgz".format(date)
        local("tar -czvf {} web_static".format(archive_path))
        return archive_path
    except:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers
    """
    if not os.path.exists(archive_path):
        return False

    file_name = os.path.basename(archive_path)
    remote_path = "/tmp/{}".format(file_name)

    put(archive_path, remote_path)

    folder_name = file_name.split(".")[0]
    run("mkdir -p /data/web_static/releases/{}".format(folder_name))
    run("tar -xzf {} -C /data/web_static/releases/{}/"
        .format(remote_path, folder_name))
    run("rm {}".format(remote_path))
    run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/"
        .format(folder_name, folder_name))
    run("rm -rf /data/web_static/releases/{}/web_static".format(folder_name))
    run("rm -rf /data/web_static/current")
    run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
        .format(folder_name))
    return True


def deploy():
    """
    Full deployment process
    """
    archive_path = do_pack()
    if archive_path is None:
        return False

    return do_deploy(archive_path)

