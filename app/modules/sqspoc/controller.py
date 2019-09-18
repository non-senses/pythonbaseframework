from flask import request, Flask, Blueprint

routes = Blueprint('sqspoc', __name__)

@routes.route('/')
def root():
    return "ROOT was called in the SqsPocController"


@routes.route('/post')
def post():
    return "POST was called in the SqsPocController"

    