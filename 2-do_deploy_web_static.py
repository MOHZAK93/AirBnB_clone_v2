#!/usr/bin/python3

from fabric.api import local, put, run, env
from datetime import datetime

env.user = "ubuntu"
env.hosts = ['3.84.239.204', '54.152.57.180']


def do_pack():
    """
    targging projects directory into a package as .tgz
    """
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    local("sudo mkdir -p ./versions")
    path = "./versions/web_static_{}".format(now)
    local("sudo tar -czvf {}.tgz web_static".format(path))
    nm = "{}.tgz".format(path)
    if nm:
        return nm
    else:
        return None


def do_deploy(archive_path):
    """
    deploys archive to web servers
    """
    try:
        archive = archive_path.split('/')[-1]
        path = '/data/web_static/releases/' + archive.strip('.tgz')
        current = '/data/web_static/current'
        put(archive_path, '/tmp')
        run('mkdir -p {}/'.format(path))
        run('tar -xzf /tmp/{} -C {}'.format(archive, path))
        run('rm /tmp/{}'.format(archive))
        run('mv {}/web_static/* {}'.format(path, path))
        run('rm -rf {}/web_static'.format(path))
        run('rm -rf {}'.format(current))
        run('ln -s {} {}'.format(path, current))
        print('New version deployed!')
        return True
    except ValueError:
        return False
