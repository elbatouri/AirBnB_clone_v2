#!/usr/bin/python3
"""
this script creates and ditributes an archive to the the server, using deploy
"""
import os
from datetime import datetime
from fabric.api import env, local, put, run, runs_once


env.hosts = ['35.153.18.223', '18.234.192.79']


@runs_once
def do_pack():
    """make a tgz archive from static files."""
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    cur_time = datetime.now()
    output = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        cur_time.year,
        cur_time.month,
        cur_time.day,
        cur_time.hour,
        cur_time.minute,
        cur_time.second
    )
    try:
        print("Packing web_static to {}".format(output))
        local("tar -cvzf {} web_static".format(output))
        archize_size = os.stat(output).st_size
        print("web_static packed: {} -> {} Bytes".format(output, archize_size))
    except Exception:
        output = None
    return output


def do_deploy(archive_path):
    """Deploys thz archive to the host servers.
    """
    if not os.path.exists(archive_path):
        return False
    file_n = os.path.basename(archive_path)
    folder_n = file_n.replace(".tgz", "")
    folder_path = "/data/web_static/releases/{}/".format(folder_n)
    success = False
    try:
        put(archive_path, "/tmp/{}".format(file_n))
        run("mkdir -p {}".format(folder_path))
        run("tar -xzf /tmp/{} -C {}".format(file_n, folder_path))
        run("rm -rf /tmp/{}".format(file_n))
        run("mv {}web_static/* {}".format(folder_path, folder_path))
        run("rm -rf {}web_static".format(folder_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder_path))
        print('New version is now LIVE!')
        success = True
    except Exception:
        success = False
    return success


def deploy():
    """Creates and dploy an archive to the host servers.
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
