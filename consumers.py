from wsgi import app
from app.modules.infrastructure.queue_service import consume_once
from time import sleep 

print("Consumers start")

while True:
    for _ in range(10):
        consume_once()


    sleep(1)
