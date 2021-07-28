from flask import Flask, request
from flasgger import Swagger

from apis.models.model import db
from apis.healthcheck import healthcheck_blueprint


def create_app(app_name='PATHS', test_config=False, production_conf=False):
    app = Flask(app_name)
    swagger = Swagger(app)
    if test_config:
        app.config.from_object('config.TestConfig')
    else:
        app.config.from_object('config.RunConfig')

    # Register api blueprints
    app.register_blueprint(healthcheck_blueprint)

    db.init_app(app)

    return app

