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

@routes.route('/clear')
def clear():
    MsrpDocument.objects.delete()
    return root()

@routes.route('/receive_product')
def receive_product():
    return "save"


@routes.route('/post')
def post():
    data = dict({
        "productCode":"some-product2",
        "countryCode": "US",
        "currencyCode": "USD",
        "includesTaxes": False,
        "amount": 121
    })

    # return data
    doc = MsrpDocument.findByUnique(**data)

    for field, value in data.items():
        doc[field] = value

    doc.save()
    return doc.to_json()



