import mongoengine
import sys
import datetime
import json
from . import helper

unique_fields = ['productCode','currencyCode','countryCode']
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
                'fields': unique_fields,
                'unique': True
            }
        ]
    }

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.utcnow()
        return super(MsrpDocument, self).save(*args, **kwargs)

    def findByUnique(**payload):
        query = dict()
        for f in MsrpDocument.getUniqueFields():
            query[f] = payload[f]

        existing = MsrpDocument.objects(**query).first()

        if None == existing:
            return MsrpDocument()

        return existing

    def to_dict(self):
        return helper.mongo_to_dict(self,[])

    def getUniqueFields():
        return unique_fields



class BasePriceCandidateDocument(mongoengine.DynamicDocument):
    ## List of valid fields https://github.com/MongoEngine/mongoengine/blob/master/mongoengine/fields.py#L61
    meta = {
        'indexes': [
            'productCode',
            'currencyCode',
            'countryCode',
            {
                'fields': unique_fields,
                'unique': True
            }
        ]
    }

    def findByUnique(**payload):
        query = dict()
        for f in BasePriceCandidateDocument.getUniqueFields():
            query[f] = payload[f]

        existing = BasePriceCandidateDocument.objects(**query).first()

        if None == existing:
            return BasePriceCandidateDocument()

        return existing

    def getUniqueFields():
        return unique_fields

    def to_dict(self):
        return helper.mongo_to_dict(self,[])


class ApprovedBasePriceDocument(mongoengine.DynamicDocument):
    ## List of valid fields https://github.com/MongoEngine/mongoengine/blob/master/mongoengine/fields.py#L61
    meta = {
        'indexes': [
            'productCode',
            'currencyCode',
            'countryCode',
            {
                'fields': unique_fields,
                'unique': True
            }
        ]
    }

    def findByUnique(**payload):
        query = dict()

        for f in ApprovedBasePriceDocument.getUniqueFields():
            print(f, payload)
            query[f] = payload[f]

        existing = ApprovedBasePriceDocument.objects(**query).first()

        if None == existing:
            return ApprovedBasePriceDocument()

        return existing

    def getUniqueFields():
        return unique_fields

    def to_dict(self):
        return helper.mongo_to_dict(self,[])


