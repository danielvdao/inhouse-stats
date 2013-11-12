from redis import Redis
from rq import Queue

queue = None

def initQueue():
    global queue
    queue = Queue(connection=Redis())

def enqueue(handler, summonerName, timeout):
    queue.enqueue_call(
        func=handler, 
        args=(summonerName,),
        timeout=timeout
    )