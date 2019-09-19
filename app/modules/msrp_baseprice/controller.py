from flask import request, Flask, Blueprint, jsonify
from app.modules.infrastructure.queue_service import QueueService, useFunctionToConsumeQueue, get_queue_names, get_queues
from datetime import datetime
from .models import MsrpDocument
import sys
import json
import http.client

routes = Blueprint('msrp-baseprice', __name__)

queue_service = QueueService()

@routes.route('/')
def root():
    return MsrpDocument.objects.to_json()


@routes.route('/post')
def post():
    data = dict({
        "countryCode": "US",
        "currencyCode": "USD",
        "includesTaxes": False,
        "amount": 123
    })

    # return data
    doc = MsrpDocument(**data)
    doc.save()

    return "save"

