import logging
from datetime import timedelta
import socket
import time

from flask import Flask, render_template, make_response, \
    request, Blueprint, redirect

from docsultant.core import app_config

logger = logging.getLogger(__name__)
logger.debug("name=" + __name__)

# TODO: move to common flask config/init file
app:Flask = None

admin_bp = Blueprint('admin_bp', __name__)



@admin_bp.route('/')
def home():
    logger.debug("home")
    return render_template('admin/home.j2')


@admin_bp.route('/inifile', methods=['GET', 'POST'])
def config():
    logger.debug("config")
    headers = {"Content-Type": "text/plain"}
    txt = ""
    index = int(request.args.get('index'))
    path = app_config.CONFIG_PATHS[index]
    if path.startswith('http'):
        return redirect(path, code=302)

    with open(path, 'r') as f:
        txt = f.read()
    return make_response(txt, 200, headers)

@admin_bp.route('/info', methods=['GET', 'POST'])
def info():
    logger.debug("info")
    d = {}
    d["Hostname"] = socket.gethostname()
    d["Uptime"] = str(timedelta(seconds=time.time() - app_config.START_TIME))
    d["Blueprints"] = str([v.import_name for k, v in app.blueprints.items()])
    return render_template('admin/info.j2', sysinfo=d)


