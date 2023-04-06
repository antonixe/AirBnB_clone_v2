#!/usr/bin/python3
"""A Fabric script to create a .tgz archive from the contents\
        of web_static folder"""
from fabric.api import local
from datetime import datetime


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
