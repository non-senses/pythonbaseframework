from flask import request, Flask, Blueprint
from app.modules.infrastructure.queue_service import QueueService, QueueServiceDecorators
import sys

routes = Blueprint('sqspoc', __name__)

queue_service = QueueService();

@routes.route('/')
def root():
    return "ROOT was called in the SqsPocController"


@routes.route('/list')
def getAll():
    return queue_service.list_queues()


@routes.route('/post')
def post():
    return (queue_service.enqueue('OneQueueName', "the message to queue"))

@QueueServiceDecorators.useFunctionToConsumeQueue('MyDefinedQueueUrl')
def consumer(message):
    sys.stdout.write("message process " + message)
    
