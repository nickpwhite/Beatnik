import os

import redis
from rq import Connection, Queue, Worker

redis_url = os.getenv('REDIS_URL')

connection = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(connection):
        worker = Worker([Queue('playlists')])
        worker.work()
