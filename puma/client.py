import logging
import os
import threading
import time
import tracemalloc
import signal


logger = logging.getLogger(__name__)


class ClientSender(threading.Thread):

        daemon = True

        def __init__(self, client, queue, interval=None):
            self.client = client
            self.snapshot_q = queue
            self.interval = interval
            super(ClientSender, self).__init__()

        def run(self):
            if hasattr(signal, 'pthread_sigmask'):
                # Available on UNIX with Python 3.3+
                signal.pthread_sigmask(signal.SIG_BLOCK, range(1, signal.NSIG))
            while True:
                if self.interval and self.snapshot_q.empty():
                    time.sleep(self.interval)
                item = self.snapshot_q.get()
                logger.info('Sending {0} snapshot file'.format(item))
                logger.info('{0} items pending to send.'.format(
                    self.snapshot_q.qsize())
                )
                snapshot = tracemalloc.Snapshot.load(item)
                self.client.send(snapshot)


class Client(object):
    def __init__(self, dsn=None):
        if dsn is None:
            dsn = os.getenv('TRACEMALLOC_DSN', None)
            if dsn is None:
                logger.info('No TRACEMALLOC_DSN found.')
        self.dsn = dsn

    def send(self, snapshot):
        logger.debug('Sending snapshot {0}'.format(snapshot))
