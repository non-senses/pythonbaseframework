from flask import Flask
from app.modules.sqspoc.controller import routes as sqs_poc_routes
import app.modules.infrastructure.queue_service

def create_app(application_name: str):
    """Initialize the core application."""
    app = Flask(application_name, instance_relative_config=False)
    app.register_blueprint(sqs_poc_routes, url_prefix='/sqspoc')    

    @app.route('/')
    def root():
        return '{appName} application running'.format(appName=application_name)

    return app