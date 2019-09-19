import os

defaults = {
    'app_name':"python-poc",
    'env': os.getenv('FLASK_ENV', "production"),
    "aws": {
        'access_key': "SOMERANDOMKEY",
        'api_secret_key': "SOMERANDOMSECRET",
        "sqs": {
            "queues": {
                "my-poc-queue":"queue-full-url",
            },
            "endpoint_url": "http://localstack:4576"
        }
    },
    'databases': {
        'mongo-default': {
            'alias': 'default',
            'db': 'pricing',
            'host': 'mongodb'
        }
    }
}

config = defaults

def isDev():
    return config['env'] == 'development'

def roleIsConsumer():
    return os.getenv('ROLE_CONSUMER', 'false').lower() != 'false'

def getDbConfig():
    return config['databases']