import boto3
import json
from config import config, isDev, roleIsConsumer
from time import sleep
from datetime import datetime
import http.client
import sys

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
            MessageBody=json.dumps(message)
        )


    def get_queue_url(self, QueueName):
        response = self.awsClient.get_queue_url(QueueName=QueueName);
        return response['QueueUrl']

    def poll_once(self, QueueName, callback):
        print("About to poll...")
        sys.stdout.write("About to poll...  STD OUT\n")
        queue = self.resourceSqs.get_queue_by_name(QueueName=QueueName)
        messages = queue.receive_messages(WaitTimeSeconds=2)
        print("Polled messages")
        sys.stdout.write("Polled...  STD OUT\n")
        for index, message in enumerate(messages):
            print("received ", index, message)
            try:
                # Start tracking time ...
                self.try_to_consume_message(message, callback)
                self.flag_message_success(message)
                # report execution time success
            except Exception as exception:
                # report exeuction time failed
                self.flag_message_failure(message, exception)

    def try_to_consume_message(self, message, callback):
        callback(message.body)

    def flag_message_success(self, message):
        message.delete()
        print("REMOVING MESSAGE")
        return True

    def flag_message_failure(self, message, exception):
        sys.stdout.write("flag_message_failure")
        print("Failure processing the message. For SQS do Nothing. Maybe send metrics?")
        print(repr(exception))
        return True

def useFunctionToConsumeQueue(QueueName):
    queue_service = QueueService()
    queue_service.ensure_queue_exists(QueueName)
    def wrapper(function_to_decorate):
        instances[QueueName] = function_to_decorate
    return wrapper

def get_queue_names():
    return json.dumps(list(instances.keys()))

def get_queues():
    return instances    