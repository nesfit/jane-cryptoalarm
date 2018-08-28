import os
import sys
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import cryptoalarm.coin as coin
import cryptoalarm.notifier as notifier

with open(os.path.dirname(__file__) + '/../config.json') as fd:
    config = json.load(fd)

    