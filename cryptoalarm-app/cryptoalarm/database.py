"""
This module specifies classes for database interactions
"""

import psycopg2
import psycopg2.extras
from datetime import datetime

class Database():
    """
    Database handles interaction with postgres
    """
    conn = None
    cursor = None

    def __init__(self, url):
        """
        Construct new Database object

        :param url: connection string
        """
        self.conn = psycopg2.connect(url)
        self.cursor = self.conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

    def get_coin(self, name):
        """
        Get dict of cryptocurrency <name>

        :param name: cryptocurrency name
        :return: dict
        """
        sql = '''
            SELECT
                id,
                name,
                explorer_url
            FROM
                coins
            WHERE
                name = %s
        '''

        self.cursor.execute(sql, (name,))
        return self.cursor.fetchone()

    def get_coins(self):
        """
        Get list of all cryptocurrencies

        :return: list of cryptocurrencies
        """
        sql = '''
            SELECT
                id,
                name,
                explorer_url
            FROM
                coins
        '''

        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_value(self, key):
        """
        Get value for <key>

        :param key: settings name
        :return: value
        """
        sql = '''
            SELECT 
                value
            FROM 
                settings
            WHERE
                key = %s
        '''

        self.cursor.execute(sql, (key,))
        return self.cursor.fetchone()['value']

    def get_addresses(self):
        """
        Get all addresse

        :return: list
        """
        sql = '''
            SELECT 
                a.id "address_id", 
                a.hash "hash", 
                c.name "coin" 
            FROM 
                addresses a 
            JOIN 
                coins c
            ON a.coin_id = c.id
            JOIN 
                watchlists w
            ON w.address_id = a.id
        '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_address_users(self, id, type):
        """
        Get users of address <id> with type <type>

        :param id: address id
        :param type: watchlist type
        :return: list
        """
        sql = '''
            SELECT 
                w.type "type", 
                w.name "watchlist_name", 
                w.notify "notify", 
                w.id "watchlist_id",
                w.email_template "email_template",
                u.id "user_id", 
                u.email "email",
                u.rest_url "rest_url"
            FROM 
                watchlists w 
            JOIN 
                users u
            ON u.id = w.user_id
            WHERE w.address_id = %s AND w.type = %s
        '''
        self.cursor.execute(sql, (id, type))
        return self.cursor.fetchall()

    def get_last_block_number(self, coin):
        """
        Get the number of last processed block of <coin>

        :param coin: Coin object
        :return: block number or 0
        """
        sql = '''
            SELECT 
                number 
            FROM 
                blocks
            WHERE 
                id = (
                    SELECT 
                        MAX(id) 
                    FROM 
                        blocks 
                    WHERE 
                        coin_id = %s
                )
        '''
        self.cursor.execute(sql, (coin.db_id,))
        result = self.cursor.fetchone()

        return result['number'] if result else 0

    def get_block_hash(self, coin, number):
        """
        Get block hash of <number> in cryptocurrency <coin>

        :param coin: Coin object
        :param number: block number
        :return: string or none
        """
        sql = '''
            SELECT 
                hash 
            FROM 
                blocks
            WHERE 
                coin_id = %s AND number = %s
        '''
        self.cursor.execute(sql, (coin.db_id, number))
        result = self.cursor.fetchone()

        return result['hash'] if result else None

    def insert_block(self, coin, number, block_hash):
        """
        Insert block of <coin>

        :param coin: Coin object
        :param number: block number
        :param block_hash: block hash
        :return: id of inserted record
        """
        sql = '''
            INSERT INTO blocks
                (coin_id, number, hash)
            VALUES
                (%s, %s, %s)
            RETURNING id
        '''
        self.cursor.execute(sql, (coin.db_id, number, block_hash))
        self.commit()
        return self.cursor.fetchone()['id']

    def delete_block(self, coin, number):
        """
        Delete block <number> of <coin>
        
        :param coin: Coin object
        :param number: block number
        """
        sql = '''
            DELETE FROM blocks
            WHERE 
                coin_id = %s AND number = %s
        '''
        self.cursor.execute(sql, (coin.db_id, number))
        self.commit()

    def insert_notifications(self, watchlist_id, txs):
        """
        Create notification for every transaction in <txs> for watchlist <watchlist_id> 

        :param watchlist_id: watchlist id
        :param txs: list of transactions
        """
        sql = 'INSERT INTO notifications (watchlist_id, block_id, tx_hash, created_at) VALUES (%s, %s, %s, %s)'
        self.cursor.executemany(sql, [(watchlist_id, tx[1], tx[2], datetime.now()) for tx in txs])
    
    def commit(self):
        """
        Commit transaction
        """
        self.conn.commit()

        
        