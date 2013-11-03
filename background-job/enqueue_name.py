from queue import redis_queue
from queue_handler import handler
import sys

TIMEOUT_IN_SECONDS = 86400 # 24 hours

def main():
    arguments = sys.argv
    if len(arguments) != 2:
        print "Expected 1 argument"
        return

    redis_queue.initQueue()
    
    redis_queue.enqueue(handler, arguments[1], TIMEOUT_IN_SECONDS)
    
if __name__ == "__main__":
    main()