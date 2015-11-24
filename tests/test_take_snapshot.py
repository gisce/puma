import time
import logging
import random

from puma import TakeSnapshot
from puma.client import ClientSender, Client

logging.basicConfig(level=logging.DEBUG)

t = TakeSnapshot(1)
t.start()

client = Client()
c = ClientSender(client, t.snapshot_q)
c.start()

while True:
    time.sleep(1)
    a = {}
    a[random.randint(0, 99999999)] = ({'x': 'j'},) * 1000
