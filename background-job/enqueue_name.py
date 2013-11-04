from queue import redis_queue
from queue_handler import handler
import sys
import time

TIMEOUT_IN_SECONDS = 86400 # 24 hours
POLL_INTERVAL = 900 # 15 minutes in seconds
PLAYER_LIST_FILENAME = 'player_list.txt'

def main():
    player_list = []
    with open(PLAYER_LIST_FILENAME) as player_list_file:
        for player in player_list_file:
            player_list.append(player.strip())
    
    print "Players:", player_list
    
    redis_queue.initQueue()
    while True:
        for player in player_list:
            print "Enqueueing", player
            redis_queue.enqueue(handler, player, TIMEOUT_IN_SECONDS)
        print "Sleeping for %s seconds" % POLL_INTERVAL
        time.sleep(POLL_INTERVAL)
    
if __name__ == "__main__":
    main()