import boto3
import json
from config import config, isDev, roleIsConsumer
from time import sleep
from datetime import datetime
import http.client

conn = http.client.HTTPSConnection('enxheluifkkri.x.pipedream.net')

instances = dict()

class QueueService:
    def __init__(self):
        self.awsClient = boto3.client(
            'sqs',
            aws_access_key_id=config["aws"]["access_key"],
            aws_secret_access_key=config["aws"]["api_secret_key"],
            endpoint_url=config["aws"]["sqs"]["endpoint_url"],
            region_name='some-region'
        )

        self.resourceSqs = boto3.resource(
            'sqs',
            aws_access_key_id=config["aws"]["access_key"],
            aws_secret_access_key=config["aws"]["api_secret_key"],
            endpoint_url=config["aws"]["sqs"]["endpoint_url"],
            region_name='some-region'
        )

    def list_queues(self):
        return self.awsClient.list_queues()

    def create_queue(self, QueueName):
        return "Creating a queue named {QueueName}".format(QueueName=QueueName)

    def ensure_queue_exists(self, QueueName):
        if isDev():
            self.awsClient.create_queue(QueueName=QueueName)

    def enqueue(self, QueueName, message):
        self.ensure_queue_exists(QueueName)

        queue_url = self.get_queue_url(QueueName)
        return self.awsClient.send_message(
            QueueUrl=queue_url,
            MessageBody=message
        )

    def get_queue_url(self, QueueName):
        response = self.awsClient.get_queue_url(QueueName=QueueName);
        return response['QueueUrl']

    def poll_once(self, QueueName, callback):
        queue = self.resourceSqs.get_queue_by_name(QueueName=QueueName)
        messages = queue.receive_messages(WaitTimeSeconds=5)

        print(messages)

        for index, message in enumerate(messages):
            print("received ", index, message)
            try:
                self.try_to_consume_message(message, callback)
                self.flag_message_success(message)
            except:
                self.flag_message_failure(message)

    def try_to_consume_message(self, message, callback):
        conn.request("POST", "/", json.dumps(message.body), {'Content-Type': 'application/json'})
        callback(message.body)

    def flag_message_success(self, message):
        message.delete()
        print("REMOVING MESSAGE")
        return True

    def flag_message_failure(self, message):
        print("For SQS do Nothing ...", handler)
        return True

def useFunctionToConsumeQueue(QueueName):
    queue_service = QueueService()
    def wrapper(function_to_decorate):
        instances[QueueName] = function_to_decorate
        print("Something is happening before the function is called.")
        ## queue_service.consume(QueueName, function_to_decorate)
        ## function_to_decorate("this is the message")
    return wrapper

def get_queue_names():
    return json.dumps(list(instances.keys()))

def get_queues():
    return instances    