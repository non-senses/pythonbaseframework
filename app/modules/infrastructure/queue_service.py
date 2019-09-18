import boto3
from config import config, isDev

print(config)

class QueueService:

    def __init__(self):
        self.awsClient = boto3.client(
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
        response = self.awsClient.get_queue_url(QueueName=QueueName);
        queue_url = response['QueueUrl']

        return self.awsClient.send_message(
            QueueUrl=queue_url,
            MessageBody=message
        )

   

class QueueServiceDecorators:
    def useFunctionToConsumeQueue(queue_path):
        def wrapper(function_to_decorate):
            print("Something is happening before the function is called.")

            function_to_decorate("this is the message")
            print("Something is happening after the function is called, see if queue is {}.".format(queue_path))

        return wrapper
