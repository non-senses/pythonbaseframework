import boto3
import json
from config import config, isDev, roleIsConsumer
from time import sleep
from datetime import datetime
import sys
from app.modules.infrastructure.logger import loggerInstance as Logger
import traceback

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

    def list_queue_names(self):
        return [x for x, _ in enumerate(instances)]

    def create_queue(self, QueueName):
        return "Creating a queue named {QueueName}".format(QueueName=QueueName)

    def ensure_queue_exists(self, QueueName):
        if isDev():
            self.awsClient.create_queue(QueueName="{}-dlq".format(QueueName))
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
        Logger.info("About to poll {}...".format(QueueName))
        queue = self.resourceSqs.get_queue_by_name(QueueName=QueueName)
        messages = queue.receive_messages(WaitTimeSeconds=2)
        Logger.info("Polled {} messages from {}...".format(len(messages), QueueName))
        print(messages)
        for index, message in enumerate(messages):
            try:
                # Start tracking time ...
                self.try_to_consume_message(message, callback)
                self.flag_message_success(message)
                # report execution time success
            except Exception as exception:
                # report exeuction time failed
                traceback.print_exc()
                self.flag_message_failure(message, exception)


    def try_to_consume_message(self, message, callback):
        body = message.body
        payload = json.loads(body)
        print("Calling callback on {}".format(payload))
        callback(payload)

    def flag_message_success(self, message):
        message.delete()
        Logger.info("Removed message")
        return True

    def flag_message_failure(self, message, exception):
        Logger.error("Errored message: {0}: {1}".format(message, repr(exception)))
        return True

    def get_queue_information_by_name(self, queue_name: str):
        return self.resourceSqs.get_queue_by_name(QueueName=queue_name).attributes


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

def consume_once():
    queue_service = QueueService()
    queues = get_queues()
    for QueueName, callback in queues.items():
        queue_service.poll_once(QueueName, callback)

