import mongoengine
import sys
import datetime

class MsrpDocument(mongoengine.Document):
    ## List of valid fields https://github.com/MongoEngine/mongoengine/blob/master/mongoengine/fields.py#L61
    productCode = mongoengine.StringField(required=True)
    includesTaxes = mongoengine.BooleanField(required=True)
    currencyCode = mongoengine.StringField(required=True)
    countryCode = mongoengine.StringField(required=True)
    amount = mongoengine.FloatField(required=True, min_value=0)
    updated_at = mongoengine.DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'indexes': [
            'productCode',
            'currencyCode',
            'countryCode',
            {
                'fields': ['productCode','currencyCode','countryCode'],
                'unique': True
            }
        ]
    }

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.utcnow()
        return super(MsrpDocument, self).save(*args, **kwargs)

    def findByUnique(**payload):
        query = dict()
        query['productCode'] = payload['productCode']
        query['countryCode'] = payload['countryCode']
        query['currencyCode'] = payload['currencyCode']
        existing = MsrpDocument.objects(**query).first()

        if None == existing:
            return MsrpDocument()

        return existing
        

