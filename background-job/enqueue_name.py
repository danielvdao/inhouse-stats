from queue import redis_queue
from queue_handler import handler
import sys

def main():
    arguments = sys.argv
    if len(arguments) != 2:
        print "Expected 1 argument"
        return

    redis_queue.initQueue()
    
    redis_queue.enqueue(handler, arguments[1], 10000)
    # TODO add timeout
    
if __name__ == "__main__":
    main()