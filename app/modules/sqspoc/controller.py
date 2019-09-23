from flask import request, Flask, Blueprint, jsonify
from werkzeug.exceptions import NotFound
from app.modules.infrastructure.queue_service import QueueService, useFunctionToConsumeQueue, get_queue_names, get_queues
from datetime import datetime
import sys
import json
import http.client

routes = Blueprint('sqspoc', __name__)

queue_service = QueueService()

@routes.route('/')
def root():
    return get_queue_names()

@routes.route('/list')
def getAll():
    return queue_service.list_queues()

@routes.route('/post')
def post_ok():
    return (queue_service.enqueue('OneQueueName', {"when": '{}'.format(datetime.now())}))

@routes.route('/post_failed')
def post_failed():
    return (queue_service.enqueue('OneQueueName', {"failed": '{}'.format(datetime.now())}))

# @useFunctionToConsumeQueue('OneQueueName')
def consumer(message) -> None:
    operation = dict({
        'originalMessage': message,
        'status': True
    })
    conn = http.client.HTTPSConnection('enxheluifkkri.x.pipedream.net')
   
    if "failed" in message:
        operation['status'] = False
        conn.request("POST", "/", json.dumps(operation), {'Content-Type': 'application/json'})
        # raise NotFound("The message failed")
        
    conn.request("POST", "/", json.dumps(operation), {'Content-Type': 'application/json', 'Connection': 'close'})


# @useFunctionToConsumeQueue('AnotherQueueName')
def consumerForAnotherQueue(message):
    sys.stdout.write("Controller::consumerForAnotherQueue, try to consume")


@routes.route('/<queue_name>')
def expose_queue_values(queue_name):
    if queue_name not in get_queue_names():
        raise NotFound('The requested queue, {}, does not exist.'.format(queue_name))

    return queue_service.get_queue_information_by_name(queue_name)


@routes.route('/consume_queues')
def consume_queues():
    queues = get_queues()
    words = list()
    for QueueName, callback in queues.items():
        queue_service.poll_once(QueueName, callback)
        words.append(QueueName)
        print("Route /consume_queues consuming " + QueueName)

    return jsonify(words)



@routes.route('/empty_queues')
def empty_queues():
    queues = queue_service.empty_all_queues()
    return json.dumps(queues)
