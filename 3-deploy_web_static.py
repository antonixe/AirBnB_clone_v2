#!/usr/bin/python3
"""
Fabric script to create and distribute an archive to web servers
"""
from fabric.api import env, run, put
from datetime import datetime
import os

env.hosts = ['100.26.154.245', '54.144.221.234']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_pack():
    """Create a compressed archive of the web_static folder"""
    try:
        if not os.path.exists("versions"):
            os.makedirs("versions")
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(now)
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except:
        return None


def do_deploy(archive_path):
    """Distribute an archive to web servers"""
    if not os.path.exists(archive_path):
        return False
    try:
        filename = os.path.basename(archive_path)
        no_extension = os.path.splitext(filename)[0]
        path = "/data/web_static/releases/{}/".format(no_extension)
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(path))
        run("tar -xzf /tmp/{} -C {}".format(filename, path))
        run("rm /tmp/{}".format(filename))
        run("mv {}web_static/* {}".format(path, path))
        run("rm -rf {}web_static".format(path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(path))
        return True
    except:
        return False


def deploy():
    """Create and distribute an archive to web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)

