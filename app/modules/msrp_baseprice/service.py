

def extract_msrps_from_product_payload(product_payload):
    product_code = product_payload['product_code']
    msrps = []

    for country, country_data in enumerate(product_payload['msrps']):
        for currency, msrp in enumerate(country_data):
            msrps.append(dict({
                'productCode': product_code,
                'countryCode': country,
                'currencyCode': currency,
                'includesTaxes': msrp['taxes_included'],
                'amount': msrp['amount']
            }))

    return msrps


