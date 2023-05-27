#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from datetime import datetime
from fabric.api import env, local, put, run
import os


env.hosts = ["18.207.1.109", "100.25.148.35"]
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder"""
    try:
        current_time = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        tgz_name = "web_static_{}.tgz".format(current_time)
        local("sudo mkdir -p versions")
        print("Packing web_static to versions/{}".format(tgz_name))
        local("sudo tar -czvf versions/{} web_static".format(tgz_name))
        return "versions/{}".format(tgz_name)
    except Exception:
        return None


def do_deploy(archive_path):
    """Distributes the archive to web servers"""
    try:
        if not os.path.exists(archive_path):
            return False

        put(archive_path, '/tmp/')

        tgzname = os.path.basename(archive_path)
        fnoext = os.path.splitext(tgzname)[0]
        run("sudo mkdir -p /data/web_static/releases/{}".format(fnoext))
        run("sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}"
            .format(tgzname, fnoext))

        run("sudo rm /tmp/{}".format(tgzname))

        run("sudo mv /data/web_static/releases/{0}/web_static/* \
/data/web_static/releases/{0}".format(fnoext))

        run("sudo rm -rf /data/web_static/releases/{}/web_static"
            .format(fnoext))

        run("sudo rm -rf /data/web_static/current")

        run("sudo ln -s /data/web_static/releases/{} /data/web_static/current"
            .format(fnoext))
        print("New version deployed!")
        return True
    except Exception:
        return False
