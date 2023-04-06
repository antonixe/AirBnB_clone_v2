#!/usr/bin/python3
"""a Fabric script that generates a .tgz archive\
        from the contents of the web_static folder\
        of your AirBnB Clone repo, using the\
        function do_pack."""
from fabric.api import local
from datetime import datetime
from os import makedirs, path


def do_pack():
    """create .tgz from web_static"""

    # create directory
    if not path.exists("versions"):
        makedirs("versions")

    # creates archive with current date and time
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = "web_static_{}.tgz".format(now)

    # compress contents of web_static into archive
    try:
        local("tar -cvzf versions/{} web_static".format(archive_name))
        return "versions/{}".format(archive_name)
    except (subprocess.CalledProcessError, OSError) as e:
        print(f"Error: {e}")
        return None