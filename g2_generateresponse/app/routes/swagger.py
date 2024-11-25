from flask import Blueprint
from flasgger import Swagger
from flask import Flask

import os


swagger_blueprint = Blueprint('swagger', __name__)

def init_swagger(app):
    app.config['SWAGGER'] = {
        'openapi': '3.0.0'
    }
    template_path = os.path.join(app.root_path, '..', 'openapi.yaml')
    swagger = Swagger(app, template_file=template_path)


@swagger_blueprint.route('/swagger/')
def serve_swagger():
    return "Swagger documentation is available at /apidocs/"

