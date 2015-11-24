import gc
import logging
import os
import pickle
import signal
import threading
import time
import tracemalloc
import multiprocessing


logger = logging.getLogger(__name__)


class TakeSnapshot(threading.Thread):
    """TakeSnapshot threading.

    :param interval: Interval of seconds between every snapshot.
    :param n_frames: Number of frames to save on the snapshot.
    """

    daemon = True

    def __init__(self, interval=60, n_frames=None):
        self.snapshot_q = multiprocessing.Queue()
        self.interval = interval
        self.n_frames = n_frames
        if self.n_frames:
            tracemalloc.start(self.n_frames)
        else:
            tracemalloc.start()
        self.counter = 1
        logger.info('Tracemalloc started')
        super(TakeSnapshot, self).__init__()

    def run(self):
        if hasattr(signal, 'pthread_sigmask'):
            # Available on UNIX with Python 3.3+
            signal.pthread_sigmask(signal.SIG_BLOCK, range(1, signal.NSIG))
        while True:
            logger.debug('Sleeping {0} secongs...'.format(self.interval))
            time.sleep(self.interval)
            filename = ("/tmp/tracemalloc-%d-%04d.dump"
                        % (os.getpid(), self.counter))
            logger.info("Write snapshot into %s..." % filename)
            gc.collect()
            snapshot = tracemalloc.take_snapshot()
            snapshot.dump(filename )
            self.snapshot_q.put(filename)
            logger.debug('Queue size: {0}'.format(self.snapshot_q.qsize()))
            snapshot = None
            logger.info("Snapshot written into %s" % filename)
            self.counter += 1
