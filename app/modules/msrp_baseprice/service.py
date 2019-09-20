

def extract_msrps_from_product_payload(product_payload):
    print("At service::extract_msrps_from_product_payload: {}".format(product_payload))
    product_code = product_payload['product_code']
    msrps = []

    msrps.append("ONE")
    msrps.append("TWO")
    return msrps

    for country, country_data in product_payload['msrps'].items():
        for currency, msrp in country_data.items():
            msrps.append(dict({
                'productCode': product_code,
                'countryCode': country,
                'currencyCode': currency,
                'includesTaxes': msrp['taxes_included'],
                'amount': msrp['amount']
            }))

    


