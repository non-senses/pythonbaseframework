from flask import Flask


def create_app(application_name: str):
    """Initialize the core application."""
    app = Flask(application_name, instance_relative_config=False)
    # app.config.from_file('./../config.py')
    
    @app.route('/')
    def root():
        return '{appName} application running'.format(appName=application_name)

    # with app.app_context():
        # Include our Routes
        # from . import routes
        
    return app