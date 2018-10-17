#!/usr/bin/env python3

import sys
import argparse
import signal
import logging
import json
from datetime import timedelta
import cryptoalarm.coin as coin
from cryptoalarm.monitor import Monitor

parser = argparse.ArgumentParser(description='Cryptoalarm')
parser.add_argument('--init', action='store_true', help='Set current blocks as last ones processed')
args = parser.parse_args()

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

with open('config.json') as fd:
    config = json.load(fd)

config['coins'] = [
    coin.BTC,
    coin.BCH,
    coin.LTC,
    coin.DASH,
    coin.ZEC,
    coin.ETH,
]

m = Monitor(config)
signal.signal(signal.SIGINT, m.shutdown)
m.test_connection()

if args.init:
    m.set_last_blocks()
else:
    m.start()
