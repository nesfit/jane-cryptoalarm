"""
This module defines classes for interactions with blockchains of cryptocurrencies 
Bitcoin, Bitcoin Cash, Litecoin, Dash, Zcash and Ethereum.
"""

import requests
import json
import time
import logging
from functools import reduce
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class Coin():
    """
    Coin specifies interface for cryptocurrency classes used in Monitor and implements wrapper for RPC calls
    """
    url = None
    block_time = None
    block = None
    reraise = False

    def __init__(self, config, stop):
        """
        Construct new Coin object

        :param config: configuration dict
        :param stop: threading.Event to signalize shutdown
        """
        self.config = config
        self.url = config['urls'][self.__class__.__name__]
        self.stop = stop
        self.transactions = {}

    def test_connection(self):
        """
        Test connection to cryptocurrency node

        :return: True for succesfull connection
        """
        self.reraise = True
        try:
            self.get_block_hash(1)
        except:
            return False
        self.reraise = False

        return True

    def get_block_time(self):
        """
        Get block time of cryptocurrency

        :return: block time
        """
        if not self.block_time:
            raise NotImplementedError
        
        return self.block_time

    def get_block_hash(self, number = None):
        """
        Get hash of block with number <number> or currently processed block

        :param number: block number
        :return: hash
        """
        raise NotImplementedError()

    def get_last_block_number(self):
        """
        Get the number of last existing block

        :return: number
        """
        raise NotImplementedError()

    def get_block_creation_time(self, number=None):
        """
        Get the creation time of block with number <number> or currently processed block

        :param number: block number
        :return: datetime
        """
        raise NotImplementedError

    def get_block(self, number):
        """
        Get block of given number

        :param number: block number
        :return: dict
        """
        raise NotImplementedError()

    def get_block_transactions(self, number = None):
        """
        Get transactions of block with number <number> or currently processed block

        :param number: block number
        :return: list of transactions
        """
        raise NotImplementedError()

    def get_transaction(self, tx_hash):
        """
        Get transaction with hash <tx_hash>

        :param tx_hash: transaction hash
        :return dict
        """
        raise NotImplementedError()

    def get_transaction_io(self, tx_hash):
        """
        Get inputs and ouputs of transation <tx_hash>

        :param tx_hash: transaction hash
        :return: dict
        """
        raise NotImplementedError()

    def rpc(self, method, *args, **kwargs):
        """
        Perform RPC call of method <method> with given arguments.

        Failed requests are repeated until data is returned or until stop event is set.
        Requests are repeated in doubling intervals until max_interval is reached.

        :param method: method name
        :param args: list of arguments for <method>
        :return:dict
        """
        retry_interval = self.config['retry_interval_min']
        headers = {'content-type': 'application/json'}
        payload = {
            'jsonrpc': '2.0',
            'method': method,
            'params': list(args),
            'id': 0,
        }

        while True:
            try:
                response = requests.post(self.url, json=payload, headers=headers, timeout=(self.config['timeout']['connect'], self.config['timeout']['read']))
                data = response.json()

                if 'error' in data and data['error']:
                    logger.error(data)
                    raise requests.exceptions.RequestException
            except Exception as e:
                if self.reraise:
                    raise e

                if self.stop.is_set(): 
                    raise InterruptedError 

                logger.warn("%s: request failed, will be repeated after %ss", self.__class__.__name__, retry_interval)
                time.sleep(retry_interval)
                retry_interval = min(retry_interval * 2, self.config['retry_interval_max'])

                continue

            if 'result' in data and data['result']:
                return data['result']
            elif self.stop.is_set(): 
                    raise InterruptedError 

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return self.__class__.__name__


class BTC(Coin):
    """
    BTC implements the intercations with Bitcoin cryptocurrency
    """
    block_time = timedelta(minutes=15)

    def get_block_hash(self, number = None):
        """
        Get hash of block with number <number> or currently processed block

        :param number: block number
        :return: hash
        """
        if number is None:
            return self.block['hash']

        return self.rpc('getblockhash', number)

    def get_last_block_number(self):
        """
        Get the number of last existing block

        :return: number
        """
        number = self.rpc('getblockcount')
        return number, self.get_block_hash(number)

    def get_block_creation_time(self, number=None):
        """
        Get the creation time of block with number <number> or currently processed block

        :param number: block number
        :return: datetime
        """
        if number is None and self.block is None:
            number, _  = self.get_last_block_number()

        if number is not None:
            self.get_block(number)

        return datetime.fromtimestamp(self.block['time'])

    def get_block(self, number):
        """
        Get block of given number

        :param number: block number
        :return: dict
        """
        block_hash = self.get_block_hash(number)
        self.block = self.rpc('getblock', block_hash, True)
        return self.block

    def get_block_transactions(self, number = None):
        """
        Get transactions of block with number <number> or currently processed block

        :param number: block number
        :return: list of transactions
        """
        if number is not None:
            self.get_block(number)

        return self.block['tx']

    def get_transaction(self, tx_hash):
        """
        Get transaction with hash <tx_hash>

        :param tx_hash: transaction hash
        :return dict
        """
        if tx_hash not in self.transactions:
            self.transactions[tx_hash] = self.rpc('getrawtransaction', tx_hash, 1)
        
        return self.transactions[tx_hash]
        
    def get_transaction_io(self, tx_hash):
        """
        Get inputs and ouputs of transation <tx_hash>

        :param tx_hash: transaction hash
        :return: dict
        """
        self.transactions = {}
        tx = self.get_transaction(tx_hash)
        vout = reduce(lambda acc, item: item['scriptPubKey'].get('addresses', []) + acc, tx['vout'], [])
        vin = reduce(lambda acc, item: self.process_inputs(item) + acc, tx['vin'], [])
        return {'in': set(vin), 'out': set(vout)}

    def process_inputs(self, input):
        """
        Find addresses used as output for each input transaction as specified by <input>

        :param input: input transaction
        :return: list of address 
        """
        if 'coinbase' in input:
            return []

        txid, index = input['txid'], input['vout']
        tx = self.get_transaction(txid)

        return tx['vout'][index]['scriptPubKey'].get('addresses', [])

class BCH(BTC):
    """
    BCH encapsulates the interactions with cryptocurrency Bitcoin Cash
    """
    block_time = timedelta(minutes=10)


class DASH(BTC):
    """
    DASH encapsulates the interactions with cryptocurrency Dash
    """
    block_time = timedelta(seconds=150)


class LTC(BTC):
    """
    LTC encapsulates the interactions with cryptocurrency Litecoin
    """
    block_time = timedelta(seconds=150)


class ZEC(BTC):
    """
    ZEC encapsulates the interactions with cryptocurrency Zcash
    """
    block_time = timedelta(seconds=150)


class ETH(Coin):
    """
    ETH encapsulates the interactions with cryptocurrency Ethereum
    """
    block_time = timedelta(seconds=15)
    ERC20_TRANSFER_PREFIX = '0xa9059cbb'

    def get_block_hash(self, number = None):
        """
        Get hash of block with number <number> or currently processed block

        :param number: block number
        :return: hash
        """
        if number is None:
            return self.block['hash']

        return self.get_block(number)['hash']

    def get_last_block_number(self):
        """
        Get the number of last existing block

        :return: number
        """        
        self.block = self.rpc('eth_getBlockByNumber', 'latest', False)
        return int(self.block['number'], 16), self.block['hash']

    def get_block_creation_time(self, number=None):
        """
        Get the creation time of block with number <number> or currently processed block

        :param number: block number
        :return: datetime
        """
        if number is not None:
            self.get_block(number)

        return datetime.fromtimestamp(int(self.block['timestamp'], 16))

    def get_block(self, number):
        """
        Get block of given number

        :param number: block number
        :return: dict
        """
        self.block = self.rpc('eth_getBlockByNumber', hex(number), False)
        return self.block

    def get_block_transactions(self, number = None):
        """
        Get transactions of block with number <number> or currently processed block

        :param number: block number
        :return: list of transactions
        """
        if number is not None:
            self.get_block(number)

        return self.block['transactions']

    def get_transaction(self, tx_hash):
        """
        Get transaction with hash <tx_hash>

        :param tx_hash: transaction hash
        :return dict
        """
        return self.rpc('eth_getTransactionByHash', tx_hash)

    def get_transaction_io(self, tx_hash):
        """
        Get inputs and ouputs of transation <tx_hash>

        :param tx_hash: transaction hash
        :return: dict
        """
        tx = self.get_transaction(tx_hash)
        result = {'in': set([tx['from']]), 'out': set([tx['to']])}
        input_data = tx['input']

        if input_data.startswith(self.ERC20_TRANSFER_PREFIX):
            recipient = '0x' + input_data[34:74]
            result['out'].add(recipient)

        return result