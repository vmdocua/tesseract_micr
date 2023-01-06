import logging
from datetime import datetime
import socket

from flask import Flask, render_template, make_response, jsonify, request, Markup

from tesseract_micr.core.app import app_init
from tesseract_micr.core.app import app_config

from tesseract_micr.admin import admin as admin
from tesseract_micr.test import test as test

logger = logging.getLogger(__name__)
logger.debug("name=" + __name__)

def create_flask_app() -> Flask:
    # move to common flask config/init file
    app_init()

    logger.info("app")

    app = Flask(__name__, template_folder='web/templates', static_folder='web/static')
    logger.debug("Loading Flask app config...")
    app.config.from_mapping(app_config.flask)

    # move to common flask config/init file
    admin.app = app

    #logging.basicConfig(level=logging.DEBUG)

    with app.app_context():
        #from .test import test

        logger.debug("Registering blueprint: admin ...")
        app.register_blueprint(admin.admin_bp, url_prefix='/admin')

        logger.debug("Registering blueprint: test ...")
        app.register_blueprint(test.test_bp, url_prefix='/test')


    @app.route('/')
    def home():
        logger.debug("home")
        return render_template('home.j2')

    return app

def main():
    app = create_flask_app()
    #app.run(debug=True)
    logger.debug("Running server ...")
    app.run(use_reloader=False)

if __name__ == "__main__":
    main()