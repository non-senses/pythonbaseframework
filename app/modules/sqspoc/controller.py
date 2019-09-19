from flask import request, Flask, Blueprint, jsonify
from werkzeug.exceptions import NotFound
from app.modules.infrastructure.queue_service import QueueService, useFunctionToConsumeQueue, get_queue_names, get_queues
from datetime import datetime
import sys
import json
import http.client

routes = Blueprint('sqspoc', __name__)

queue_service = QueueService()

def debug(message):
    conn = http.client.HTTPSConnection('enxheluifkkri.x.pipedream.net')
    conn.request("POST", "/", json.dumps(message), {'Content-Type': 'application/json'})

@routes.route('/')
def root():
    return "ROOT was called in the SqsPocController"

@routes.route('/list')
def getAll():
    return queue_service.list_queues()

@routes.route('/post')
def post_ok():
    return (queue_service.enqueue('OneQueueName', {"when": '{}'.format(datetime.now())}))

@routes.route('/post_failed')
def post_failed():
    return (queue_service.enqueue('OneQueueName', {"failed": '{}'.format(datetime.now())}))


@useFunctionToConsumeQueue('OneQueueName')
def consumer(message) -> None:
    sys.stdout.write("Controller::consumer, try to consume:")
    debug(message)
    if "failed" in message:
        raise NotFound("The message failed")

    sys.stdout.write("...consumed")

@useFunctionToConsumeQueue('AnotherQueueName')
def consumerForAnotherQueue(message):
    sys.stdout.write("Controller::consumerForAnotherQueue, try to consume")
    debug(message)
    sys.stdout.write("...consumed")

@routes.route('/get_queues')    
def expose_queues():
    print("doing something")
    return get_queue_names()

@routes.route('/consume_queues')
def consume_queues():
    queues = get_queues()
    words = list()
    for QueueName, callback in queues.items():
        queue_service.poll_once(QueueName, callback)
        words.append(QueueName)
        print("Route /consume_queues consuming " + QueueName)

    return jsonify(words)



