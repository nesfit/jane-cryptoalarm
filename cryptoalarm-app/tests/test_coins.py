#!/usr/bin/env python3

import unittest
import logging
import json
from datetime import datetime
from types import MethodType
from context import coin, config

class TestBTC(unittest.TestCase):

    def setUp(self):
        config['coins'] = [coin.BTC]
        self.coin = coin.BTC(config, None)

    def test_get_block_hash(self):
        result = self.coin.get_block_hash(50001)
        self.assertEqual(result, '000000001c920d495e1eeef2452b6d1c6c229a919b28196c103ecffebabee141')

    def test_get_block_creation_time(self):
        result = self.coin.get_block_creation_time(50001)
        self.assertEqual(result, datetime(2010, 4, 10, 18, 31, 40))

    def test_get_block_transactions(self):
        txs = [
            'e1882d41800d96d0fddc196cd8d3f0b45d65b030c652d97eaba79a1174e64d58', 
            '7940cdde4d713e171849efc6bd89939185be270266c94e92369e3877ad89455a', 
            'f84761459a00c6df3176ae5d94c99e69f25100d09548e5686bd0c354bb8cc60a'
        ]

        result = self.coin.get_block_transactions(50001)
        self.assertEqual(result, txs)

    def test_get_transaction_io_multiple_in(self):
        addresses = {
            'in': set(['1DoQeKfU3dYhN9bxMpFFcVUnufCPDqSPae', '1PZMgkF2x161qvfP7dhoWSEEU3SjnQE1m9']),
            'out': set(['1HaHTfmvoUW6i6nhJf8jJs6tU4cHNmBQHQ']),
        }

        result = self.coin.get_transaction_io('7940cdde4d713e171849efc6bd89939185be270266c94e92369e3877ad89455a')
        self.assertEqual(result, addresses)

    def test_get_transaction_io_multiple_out(self):
        addresses = {
            'in': set(['1BNwxHGaFbeUBitpjy2AsKpJ29Ybxntqvb']),
            'out': set(['1JqDybm2nWTENrHvMyafbSXXtTk5Uv5QAn', '1EYTGtG4LnFfiMvjJdsU7GMGCQvsRSjYhx']),
        }

        result = self.coin.get_transaction_io('fff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4')
        self.assertEqual(result, addresses)

class TestETH(unittest.TestCase):
    def setUp(self):
        config['coins'] = [coin.ETH]
        self.coin = coin.ETH(config, None)

    def test_get_block_hash(self):
        result = self.coin.get_block_hash(50006)
        self.assertEqual(result, '0x6d3d859f7aa4b95088a2d7e7b5e0e62e046877737d6a190ac7b889e86688ff0d')

    def test_get_block_creation_time(self):
        result = self.coin.get_block_creation_time(50006)
        self.assertEqual(result, datetime(2015, 8, 7, 23, 24, 47))

    def test_get_block_transactions(self):
        txs = ['0xde883448ecf0904071953e0382ef401e9bc44b8a3ea3769f7f9e5c15c0b6d29d']

        result = self.coin.get_block_transactions(50006)
        self.assertEqual(result, txs)

    def test_get_transaction_io(self):
        addresses = {
            'in': set(['0xef61bdd3730e2a710e4028bed38bff7f8efabc33']),
            'out': set(['0xd13d21cf4925ce6ef39681ba2b6ff01f2f53813b', '0xf3b3cad094b89392fce5fafd40bc03b80f2bc624']),
        }

        result = self.coin.get_transaction_io('0x7647cde28f67d73b7312744e4bbb37d84e1d6109d4eec4ac19c574456373b81f')
        self.assertEqual(result, addresses)


if __name__ == '__main__':
    unittest.main()