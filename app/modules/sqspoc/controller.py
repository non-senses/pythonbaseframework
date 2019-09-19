from flask import request, Flask, Blueprint
from app.modules.infrastructure.queue_service import QueueService, useFunctionToConsumeQueue, get_queue_names, get_queues
import sys
import json
import http.client

conn = http.client.HTTPSConnection('enxheluifkkri.x.pipedream.net')


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

@useFunctionToConsumeQueue('OneQueueName')
def consumer(message):
    conn.request("POST", "/", '<<CONSUMER>> '+message+'</CONSUMER>', {'Content-Type': 'application/json'})
    sys.stdout.write("message process " + message)
    
@routes.route('/get_queues')    
def expose_queues():
    print("doing something")
    return get_queue_names()

@routes.route('/consume_queues')
def consume_queues():
    queues = get_queues()
    for QueueName, callback in queues.items():
        queue_service.poll_once(QueueName, callback)
        print(QueueName)

    return "yep!"
    


