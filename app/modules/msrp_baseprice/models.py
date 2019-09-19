import mongoengine

class MsrpDocument(mongoengine.Document):
    includesTaxes = mongoengine.BooleanField(required=True)
    currencyCode = mongoengine.StringField(required=True)
    countryCode = mongoengine.StringField(required=True)
    amount = mongoengine.FloatField(required=True, min_value=0)

