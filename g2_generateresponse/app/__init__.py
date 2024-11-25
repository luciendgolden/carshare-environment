from flask import Flask
from flask_cors import CORS
from .config import Config

from .services.graphdb import repo_exists, create_repo, preload_rdf

from .routes.home import home_blueprint
from .routes.request import request_management_blueprint
from .routes.database import db_operations_blueprint
from .routes.swagger import swagger_blueprint, init_swagger
from .routes.health import health_blueprint

import logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Set the logging level of the app logger
    app.logger.setLevel(logging.DEBUG)
    
    CORS(app)

    logging.debug('This is a debug message from the startup.')

    app.register_blueprint(home_blueprint, url_prefix='/')
    app.register_blueprint(request_management_blueprint, url_prefix='/request')
    app.register_blueprint(db_operations_blueprint, url_prefix='/db')
    app.register_blueprint(swagger_blueprint, url_prefix='/')
    app.register_blueprint(health_blueprint, url_prefix='/')

    init_swagger(app)

    with app.app_context():
        if not repo_exists():
            create_result = create_repo()
            app.logger.info(f"Create result {create_result}")
            schema_result = preload_rdf('schema.ttl')
            app.logger.info(f"Schema preload res2ult {schema_result}")
            data_result = preload_rdf('data.ttl')
            app.logger.info(f"Data preload result {data_result}")

    return app
