#!/usr/bin/env python3

import sys
import json
import threading
from cryptoalarm.coin import BTC, BCH, DASH, ZEC, LTC, ETH

def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


ticker = sys.argv[1]
method = sys.argv[2]

with open('config.json') as fd:
    config = json.load(fd)

coin = globals()[ticker](config, threading.Event())
args = [int(item) if is_int(item) else item for item in sys.argv[3:]]
result = getattr(coin.__class__, method)(coin, *args)

if isinstance(result, dict):
    print(json.dumps(result, indent=4))
else:
    print(result)