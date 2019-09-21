from flask import request, Flask, Blueprint, jsonify
from app.modules.infrastructure.queue_service import QueueService, useFunctionToConsumeQueue, get_queue_names, get_queues
from datetime import datetime
from app.modules.infrastructure.queue_service import QueueService, useFunctionToConsumeQueue
from .models import MsrpDocument, BasePriceCandidateDocument
import sys
import json
import http.client
import random
from . import service as msrpService

routes = Blueprint('msrp-baseprice', __name__)

queue_service = QueueService()


@routes.route('/base-price-candidates')
def bpc_root():
    return BasePriceCandidateDocument.objects.to_json()

@routes.route('/msrps')
def msrp_root():
    return MsrpDocument.objects.to_json()

@routes.route('/clear')
def clear():
    MsrpDocument.objects.delete()
    return root()

@routes.route('/pretend_a_product_was_updated', methods=['POST'])
def receive_product():
    payload = request.get_json()
    return queue_service.enqueue('the-pim-queue', payload)
    

@routes.route('/test_single/<product_code>')
def test_receive_product(product_code):
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
    return json.dumps(msrpService.extract_msrps_from_product_payload(product))

@useFunctionToConsumeQueue('the-pim-queue')
def consume_a_message_from_products_queue(message):
    msrps = msrpService.extract_msrps_from_product_payload(message)
    responses = []
    for single_msrp in msrps:
        print(single_msrp)
        doc = msrpService.import_msrp_if_newer(single_msrp)
        queue_service.enqueue('base-price-candidate-generator', doc)
        responses.append(doc)

    print(responses)



@useFunctionToConsumeQueue('base-price-candidate-generator')
def build_candidate_from_msrp(payload):
    msrp_with_process_data = msrpService.enrich_process_data(payload)
    print("a data-complete price looks like this: {}".format(msrp_with_process_data))

    msrp_with_result_data = msrpService.compute_result(msrp_with_process_data)
    print("a computed price price looks like this: {}".format(msrp_with_result_data))
    
    return msrpService.persist_base_price_candidate(msrp_with_result_data)


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


@routes.route('/mock-pim-payload')
def mock_pim_payload():
    countries = random.sample(['CA','US','FR','AR','JP'], int(2+random.randrange(0,3)))
    currencies = random.sample(['CAD','USD','EUR','RIN','AR$'], int(3+random.randrange(0,2)))
    howManyCurrencies = 1

    mocked_msrp = {
        "product_code": oct(random.randint(0,5000)),
        "msrps": {}
    }

    for country in countries:
        if random.random() < .05:
            continue

        mocked_msrp['msrps'][country] = {}
        for currency in currencies:
            if random.random() < .05:
                continue

            amount = random.randrange(100, 1900)
            taxes_included = random.random() < .4

            mocked_msrp['msrps'][country][currency] = {
                "amount": amount,
                "taxes_included": taxes_included
            }
        
    return mocked_msrp



@routes.route('/mock-pim-calls')
def fake_multiple_products():
    for i in range(250):
        queue_service.enqueue('the-pim-queue', mock_pim_payload())