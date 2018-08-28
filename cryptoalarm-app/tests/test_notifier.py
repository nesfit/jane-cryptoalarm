#!/usr/bin/env python3

import unittest
import logging
from datetime import datetime
from types import MethodType
from context import coin, notifier, config


class TestNotifier(unittest.TestCase):

    watchlist_id = 1
    user_id = 2
    block_id = 3
    address_id = 4
    block_number = 10
    tx_hash = '0x7647cde28f67d73b7312744e4bbb37d84e1d6109d4eec4ac19c574456373b81f'
    address_hash = '0xd13d21cf4925ce6ef39681ba2b6ff01f2f53813b'

    def setUp(self):
        config['coins'] = [coin.ETH]
        test_coin = coin.ETH(config, None)
        self.notifier = notifier.Notifier(config, DatabaseMock())
        for sender in self.notifier.senders:
            sender.send = MethodType(lambda x: None, sender) 

        addresses = {
            'in': set(['0xf3b3cad094b89392fce5faf234232342342343']),
            'out': set([self.address_hash, '0xf3b3cad094b89392fce5fafd40bc03b80f2bc624']),
        }
        self.notifier.process_transaction(test_coin, self.block_number, self.block_id, self.tx_hash, addresses)
        
        self.notifier.notify()

    def test_watchlist(self):
        self.assertEqual(self.notifier.data['ETH']['data'][self.address_hash]['users']['inout'][0]['watchlist_id'], 1)

    def test_process_transaction(self):
        self.assertTrue((self.block_number, self.block_id, self.tx_hash) in self.notifier.data['ETH']['data'][self.address_hash]['txs']['out'])

    def test_unique_notification_inout(self):
        for sender in self.notifier.senders:
            self.assertEqual(len(sender.queue), 1)
        
class DatabaseMock():

    def get_setting(self, key):
        return 'value'

    def get_coins(self):
        return [{'name': 'ETH', 'explorer_url': 'url'}]

    def get_addresses(self):
        return [{'address_id': TestNotifier.address_id, 'hash': TestNotifier.address_hash, 'coin': 'ETH'}]

    def get_address_users(self, id, type):
        if type != 'inout':
            return []

        return [{
            'type': 'inout', 
            'watchlist_name': 'mock', 
            'notify': 'both', 
            'watchlist_id': TestNotifier.watchlist_id,
            'email_template': 'mock',
            'user_id': TestNotifier.user_id,
            'email': 'mock@email',
            'rest_url': 'mock.url'
        }]

    def insert_notifications(self, watchlist_id, txs):
        pass
    
    def commit(self):
        pass


if __name__ == '__main__':
    unittest.main()