from .models import MsrpDocument, BasePriceCandidateDocument, ApprovedBasePriceDocument
from functools import reduce
import random
import json
import datetime

def extract_msrps_from_product_payload(product_payload):
    product_code = product_payload['product_code']
    msrps = []

    for country, country_data in product_payload['msrps'].items():
        for currency, msrp in country_data.items():
            msrps.append(dict({
                'productCode': product_code,
                'countryCode': country,
                'currencyCode': currency,
                'includesTaxes': msrp['taxes_included'],
                'amount': msrp['amount']
            }))
    
    print("** Extracted these MSRPS:")
    print(msrps)
    return msrps

    

def import_msrp_if_newer(msrp_data):
    doc = MsrpDocument.findByUnique(**msrp_data)

    for f in ['productCode', 'countryCode', 'currencyCode', 'includesTaxes', 'amount']:
        doc[f] = msrp_data[f]
    
    doc.save()
    return doc.to_dict()
    
def persist_base_price_candidate(base_price_candidate):
    doc = BasePriceCandidateDocument.findByUnique(**base_price_candidate)
    for field, value in base_price_candidate.items():
        doc[field] = value

    doc.save()


def enrich_process_data(raw_msrp):
    enriched_data = raw_msrp # copy all data
    enriched_data['process_data'] = {
        'costs': get_enriched_costs(raw_msrp),
        'duties': get_enriched_duties(raw_msrp),
        'taxes': get_enriched_taxes(raw_msrp)
    }
    return enriched_data


def compute_result(msrp_data):
    computed_price_candidate = msrp_data
    initial_price = build_initial_price(computed_price_candidate)
    computed_price_candidate['process_results'] = {
        'initial-price': initial_price
    }

    base_price = build_base_price(computed_price_candidate)
    computed_price_candidate['process_results'] = {
        'initial-price': initial_price,
        'base-price': base_price,
    }
    return computed_price_candidate


def build_initial_price(msrp_data):
    initial = msrp_data['amount']
    if not msrp_data['includesTaxes']:
        return {
            'currencyCode': msrp_data['currencyCode'],
            'amount': initial,
            'reason':'Taxes were not included in the MSRP'
        }    

    for tax in msrp_data['process_data']['taxes']:
        initial -= tax['amount']

    return {
        'currencyCode': msrp_data['currencyCode'],
        'amount': initial,
        'reason':'Taxes are included in the MSRP. Initial price should be smaller'
    }


def build_base_price(msrp_data):
    base = msrp_data['process_results']['initial-price']['amount']

    if msrp_data['countryCode'] in ['CA']:
        return {
            'currencyCode': msrp_data['currencyCode'],
            'amount': base,
            'reason': 'Duties are free in CA'
        }


    if None in msrp_data['process_data']['duties']:
        return {
            'currencyCode': msrp_data['currencyCode'],
            'amount': base,
            'reason': 'No duties found for this country'
        }

    for duty in msrp_data['process_data']['duties']:
        base -= duty['amount']

    return {
        'currencyCode': msrp_data['currencyCode'],
        'amount': base,
        'reason': 'Duties were subtracted from the initial price'
    }

def get_enriched_costs(msrp_data):
    return [
        retrieve_cost(msrp_data),
        {
            'amount': random.random(),
            'currencyCode': msrp_data['currencyCode']
        }
    ]

def get_enriched_duties(msrp_data):
    return [
        retrieve_tax_or_duty(msrp_data)
    ]

def get_enriched_taxes(msrp_data):
    taxes = [
        retrieve_tax_or_duty(msrp_data)
    ]

    if msrp_data['countryCode'] == 'CA':
        # Pretend some province tax
        rate = 0.05 + random.random() * 0.5

        taxes.append({
            'rate': rate,
            'amount': msrp_data['amount'] * rate,
            'description': 'Province tax'
        })

        if random.random() < .5:
            rate = 0.05 + random.random() * 0.5
            taxes.append({
                'rate': rate,
                'amount': msrp_data['amount'] * rate,
                'description': 'A random tax'
            })            

    return taxes

def retrieve_cost(msrp_data):
    ## Pretend a cost...
    margin = .2 + random.random() * .4
    cost = msrp_data['amount'] * margin
    return dict({
        'amount': cost,
        'currencyCode': msrp_data['currencyCode']
    })


def retrieve_tax_or_duty(msrp_data):
    ## Pretend a tax or a duty...
    rate = .03 + random.random() * .4
    cost = msrp_data['amount'] * rate
    return dict({
        'rate': rate,
        'amount': cost,
        'currencyCode': msrp_data['currencyCode']
    })


def approve_a_candidate(candidate_id):
    candidate = BasePriceCandidateDocument.objects.get(id=candidate_id)

    if candidate is None:
        raise Exception("Candidate not found")

    candidate_as_dict = candidate.to_dict()

    approved = ApprovedBasePriceDocument.objects(countryCode=candidate['countryCode'], currencyCode=candidate['currencyCode'], productCode=candidate['productCode']).first()
    if approved is None:
        approved = ApprovedBasePriceDocument()

    for f in ['countryCode', 'currencyCode', 'productCode', 'process_data', 'process_results']:
        approved[f] = candidate[f]
    
    approved['approved_at'] = datetime.datetime.utcnow()
    approved.save()

    candidate.modify(approved=True)
    return approved.to_json()



def reject_a_candidate(candidate_id):
    candidate = BasePriceCandidateDocument.objects.get(id=candidate_id)

    if candidate is None:
        raise Exception("Candidate not found")

    candidate.modify(approved=False)
    candidate.save()
    return candidate.to_json()


        
