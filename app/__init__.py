from flask import Flask
from app.modules.sqspoc.controller import routes as sqs_poc_routes
from app.modules.msrp_baseprice.controller import routes as msrp_baseprice_routes
from app.modules.infrastructure.mongo_service import dbConnection

def create_app(application_name: str):
    """Initialize the core application."""
    app = Flask(application_name, instance_relative_config=False)
    
    app.register_blueprint(sqs_poc_routes, url_prefix='/sqspoc')
    app.register_blueprint(msrp_baseprice_routes, url_prefix='/msrp-baseprice')

    @app.route('/')
    def root():
        return '{appName} application running'.format(appName=application_name)

    return app