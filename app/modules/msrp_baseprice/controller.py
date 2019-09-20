from flask import request, Flask, Blueprint, jsonify
from app.modules.infrastructure.queue_service import QueueService, useFunctionToConsumeQueue, get_queue_names, get_queues
from datetime import datetime
from app.modules.infrastructure.queue_service import QueueService, useFunctionToConsumeQueue
from .models import MsrpDocument
import sys
import json
import http.client
import random
from . import service as msrpService

routes = Blueprint('msrp-baseprice', __name__)

queue_service = QueueService()

@routes.route('/')
def root():
    return MsrpDocument.objects.to_json()

@routes.route('/clear')
def clear():
    MsrpDocument.objects.delete()
    return root()

@routes.route('/pretend_a_product_was_updated/<product_code>')
def receive_product(product_code):
    product = dict({
        "product_code": "product_code_{}".format(product_code),
        "msrps": {
            "US": {
                "USD": {
                    "taxes_included": True,
                    "amount": random.randrange(50, 60)
                }
            },
            "CA": {
                "CAD": {
                    "taxes_included": False,
                    "amount": random.randrange(60, 70)
                },
                "USD": {
                    "taxes_included": False,
                    "amount": random.randrange(40, 50)
                },                
            },            
        }
    })
    return queue_service.enqueue('the-pim-queue', product)

@useFunctionToConsumeQueue('the-pim-queue')
def consume_a_message_from_products_queue(message):
    data = msrpService.extract_msrps_from_product_payload(message)
    print(data)
    conn = http.client.HTTPSConnection('enxheluifkkri.x.pipedream.net')
    conn.request("POST", "/", json.dumps(data), {'Content-Type': 'application/json'})
    return "e"

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



