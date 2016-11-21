"""
A  very simple distribute lock base on single distributed redis
"""
import time
import uuid
import math

import redis


class DistroLock(object):

    def __init__(self, conn, lockname, lock_timeout=10):
        """
        :param conn: redis connection
        :param lockname: distributed lock identify lockname
        :param lock_timeout: max time(in second) client can hold the lock
        """
        self.conn = conn
        self.lockname = 'distribute:lock:py:{}'.format(lockname)
        self.lock_timeout = lock_timeout

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()

    def __delete__(self):
        self.release()

    def acquire(self, timeout=5):
        """
        :param timeout: max time(in secode) acquire lock
        """
        identifier = str(uuid.uuid4())
        lock_timeout = int(math.ceil(self.lock_timeout))

        end = time.time() + timeout
        while time.time() < end:
            if self.conn.setnx(self.lockname, identifier):
                self.conn.expire(self.lockname, lock_timeout)
                self.identifier = identifier
                return True

            elif not self.conn.ttl(self.lockname):
                self.conn.expire(self.lockname, lock_timeout)

        return False

    def release(self):
        pipe = self.conn.pipeline()

        while True:
            try:
                pipe.watch(self.lockname)
                if pipe.get(self.lockname).decode() == self.identifier:
                    pipe.multi()
                    pipe.delete(self.lockname)
                    pipe.execute()
                    return True
                pipe.unwatch()
                break
            except redis.exceptions.WatchError as err:
                pass

        return False
