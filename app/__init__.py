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
        return '</br>'.join([
            '{appName} application running'.format(appName=application_name),
            "",
            "Some routes you might want to check:",
            "/sqspoc to list the queues we monitor across the entire application",
            "/sqspoc/<any queue name> to gather information about that queue",
            "",
            "MSRP Magic",
            ## "/msrp-baseprice/msrps to see all the available MSRPs we've ever received from PIM"

            ])
        

    return app