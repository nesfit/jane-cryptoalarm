"""
This module speficies class Notifier for transaction processing based on specified watchlists.
"""

import logging
import smtplib
import requests
import queue
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
import time
import re

logger = logging.getLogger(__name__)

class Notifier():
    """
    Notifier handles transaction processing based on specified watchlists
    """
    queue = queue.Queue()
    data = {}
    database = None
    senders = []
    last_notify = None
    last_load = None

    def __init__(self, config, database):
        """
        Construct new Notifier objects

        :param config: configuration dict
        :param database: Database object
        """
        self.database = database
        self.config = config
        self.load()
        self.last_notify = datetime.now()

        mailer = Mailer(config,
            self.config['notifier']['email_subject'], 
            self.config['notifier']['email_from'], 
            self.config['notifier']['email_template']
        )
        self.senders = [mailer, Rest()]

    def test_connection(self):
        """
        Test connection of each notification sender
        """
        for sender in self.senders:
            sender.test_connection()

    def load(self):
        """
        Load information about watched addresses and its users
        """
        logger.debug('load')
        self.data = {}

        for coin in self.database.get_coins():
            self.data[coin['name']] = {
                'explorer_url': coin['explorer_url'],
                'data': {},
            }

        for address in self.database.get_addresses():
            if not address['hash'] in self.data[address['coin']]['data']:
                self.data[address['coin']]['data'][address['hash']] = {
                    'txs': {'in': set(), 'out': set()},
                    'users': {'in': [], 'out': [], 'inout': []},
                }

            ptr = self.data[address['coin']]['data'][address['hash']]

            for type in ['in', 'out', 'inout']:
                ptr['users'][type] = self.database.get_address_users(address['address_id'], type)

        self.last_load = datetime.now()

    def add_transaction(self, coin, block_number, block_id, hash, addresses):
        """
        Insert transaction in processing queue

        :param coin: Coin object
        :param block_number: number of block that includes given transaction
        :param block_id: id of block record in database
        :param hash: transaction hash
        :param addresses: dict of input and output addresses of transaction
        """
        #print(coin, block_number, block_id, hash, addresses)
        self.queue.put((coin, block_number, block_id, hash, addresses))

    def worker(self, stop):
        """
        Indefinetly process transactions in queue

        :param stop: threading.Event to signalize shutdown
        """
        #print(self.queue)
        while not stop.is_set() or not self.queue.empty(): 

            try:
                coin, block_number, block_id, hash, addresses = self.queue.get(timeout=self.config['notify_interval'])
                self.process_transaction(coin, block_number, block_id, hash, addresses)
                self.queue.task_done()
                
            except queue.Empty:
                self.notify()
                continue
                       
            if self.last_notify + timedelta(seconds=self.config['notify_interval']) < datetime.now():
                self.notify()

            if self.last_load + timedelta(seconds=self.config['reload_interval']) < datetime.now():
                self.load()

    def process_remaining(self):
        """
        Process transaction inserted in queue after shutdown was signalized
        """
        logger.info('sending remaining notifications')

        while not self.queue.empty(): 
            coin, block_number, block_id, hash, addresses = self.queue.get()
            self.process_transaction(coin, block_number, block_id, hash, addresses)
        
        self.notify()

    def process_transaction(self, coin, block_number, block_id, hash, addresses):
        """
        Save transaction that involve addresses specified in watchlist

        :param coin: Coin object
        :param block_number: number of block that includes given transaction
        :param block_id: id of block record in database
        :param hash: transaction hash
        :param addresses: dict of input and output addresses of transaction
        """
        coin_name = str(coin)
        #print(coin, block_number, block_id, hash, addresses)
        #print(self.data[coin_name]['data'].keys())
        for type in ['in', 'out']:
            intersect = set(self.data[coin_name]['data'].keys()) & addresses[type]
            #print(intersect)
            for address in intersect:
                self.data[coin_name]['data'][address]['txs'][type].add((block_number, block_id, hash))

    def notify(self):
        """
        Notify users about transactions involving monitored addresses
        """
        logger.info('notify')

        for coin_name in self.data:
            for address, address_data in self.data[coin_name]['data'].items():
                explorer_url = self.data[coin_name]['explorer_url']
                # notify users with INOUT about IN and OUT tranasctions
                if address_data['txs']['out'] or address_data['txs']['in']:
                    for user in address_data['users']['inout']: 
                        self.add(coin_name, explorer_url, user, address, address_data['txs']['out'] | address_data['txs']['in'])

                if address_data['txs']['out']:
                    for user in address_data['users']['out']: 
                        self.add(coin_name, explorer_url, user, address, address_data['txs']['out'])

                if address_data['txs']['in']:
                    for user in address_data['users']['in']: 
                        self.add(coin_name, explorer_url, user, address, address_data['txs']['in'])

                address_data['in'] = set()
                address_data['out'] = set()
        
        #print(self.senders)
        for sender in self.senders:
            sender.send()

        self.database.commit()
        self.last_notify = datetime.now()       

    def add(self, coin, explorer_url, user, address, txs):
        """
        Submit <address>'s transactions to notify queue of all senders

        :param coin: Coin object
        :param explorer_url: string of url of blockchain explorer
        :param user: dict with user information
        :param address: address hash
        :param txs: list of transaction address was involved in
        """
        logger.debug('notify.add')
        #print(coin, user, txs)
        logger.debug('%s: add notification for user %s about %s', coin, user, txs)
               
        self.database.insert_notifications(user['watchlist_id'], txs)
        
        for sender in self.senders:            
            if user['notify'] in sender.types:
                logger.debug('notify.adding a new txs')
                sender.add(coin, explorer_url, user, address, txs)

class Sender():
    """
    Sender defines the interface for each type of notification sender
    """
    types = []

    def add(self, coin, explorer_url, user, address, txs):
        """
        Submit <address>'s transactions to notify queue

        :param coin: Coin object
        :param explorer_url: string of url of blockchain explorer
        :param user: dict with user information
        :param address: address hash
        :param txs: list of transaction address was involved in
        """
        #self.queue.append((coin, explorer_url, user, address, list(txs)))
        raise NotImplementedError()

    def send(self):
        """
        Send notifications
        """
        raise NotImplementedError()
    
    def test_connection(self):
        """
        Test connectivity
        """
        pass


class Mailer(Sender):
    """
    Mailer encapsulates the generation of email messages from notification
    """
    server = None
    template = None
    email = None
    subject = None
    types = ['email', 'both']

    def __init__(self, config, subject, email, template):
        """
        Construct new Mailer object

        :param confog: configuration dict
        :param subject: string
        :param email: source email
        :param template: default email template
        """
        self.queue = []
        self.config = config
        self.email = email
        self.subject = subject
        self.template = template
    
    def test_connection(self):
        """
        Test connection of SMTP server
        """
        self.connect()
        self.server.quit()

    def add(self, coin, explorer_url, user, address, txs):
        """
        Submit <address>'s transactions to notify queue

        :param coin: Coin object
        :param explorer_url: string of url of blockchain explorer
        :param user: dict with user information
        :param address: address hash
        :param txs: list of transaction address was involved in
        """                     
        logger.debug('mailer.add')
        self.queue.append((coin, explorer_url, user, address, list(txs)))

    def connect(self):
        """
        Connet to SMTP server
        """
        if self.config['smtp']['ssl'] == "tls":
            self.server = smtplib.SMTP_SSL(self.config['smtp']['server'], self.config['smtp']['port'])
        elif self.config['smtp']['ssl'] == "starttls":
            self.server = smtplib.SMTP(self.config['smtp']['server'], self.config['smtp']['port'])
            self.server.starttls()
        else:
            self.server = smtplib.SMTP(self.config['smtp']['server'], self.config['smtp']['port'])        
        
        #self.server.set_debuglevel(10)        
        result = self.server.login(self.config['smtp']['username'], self.config['smtp']['password'])
        logging.info(result)

    def build_body(self, coin, explorer_url, user, address, txs):
        """
        Build notification body

        :param coin: Coin object
        :param explorer_url: string of url of blockchain explorer
        :param user: dict with user information
        :param address: address hash
        :param txs: list of transactions
        :return: notification dict
        """
        template = self.template
        if user['email_template']:
            template = user['email_template']

        txs_links = []
        #print(txs)
        txs = sorted(txs, key=lambda tx: tx[1])
        #print(txs)
        for block_number, block_id, tx in txs:
            tx_url = self.config['notifier']['server'] + coin + '/tx/' + tx
            txs_links.append('#{} <a href="{}">{}</a><br>'.format(block_number, tx_url, tx))

        address_url = self.config['notifier']['server'] + coin + '/addr/' + address
        address_str = '<a href="{}">{}</a>'.format(address_url, address)

        return template.format(address=address_str, coin=coin, name=user['watchlist_name'], txs='\n'.join(txs_links))

    def build_message(self, coin, explorer_url, user, address, txs):
        """
        Build email notification

        :param coin: Coin object
        :param explorer_url: string of url of blockchain explorer
        :param user: dict with user information
        :param address: address hash
        :param txs: list of transactions
        :return: notification string
        """
        body = self.build_body(coin, explorer_url, user, address, txs)
        part1 = MIMEText(re.sub('<[^<]+?>', '', body), 'plain')
        part2 = MIMEText('<html>'+body+'</html>', 'html')
        msg = MIMEMultipart('alternative')
        msg.attach(part1)
        msg.attach(part2)
        msg['Subject'] = self.subject.format(coin=coin, name=user['watchlist_name'])
        msg['From'] = self.email
        msg['To'] = user['email']
        msg['Date'] = formatdate(time.time())
        return msg.as_string()

    def send(self):
        """
        Send notifications
        """
        logger.info('mail.send')
        
        if self.queue:
            #print(self.queue)  
            try:
                self.connect()            
                while self.queue:
                    coin, explorer_url, user, address, txs = self.queue.pop()
                    message = self.build_message(coin, explorer_url, user, address, txs)
                    self.server.sendmail(self.email, [user['email']], message)
                    logger.info('MAIL successfully sent')
                self.server.quit()          
            except Exception as e:
                logger.warn(e)
                logger.warn('MAIL failed')
                
        self.queue = []
        
class Rest(Sender):
    """
    Rest encapsulates the generation of rest notifications
    """
    types = ['rest', 'both']

    def __init__(self):
        """
        Construct new Rest object
        """
        self.queue = []
    
    def add(self, coin, explorer_url, user, address, txs):
        """
        Submit <address>'s transactions to notify queue only if user specified rest url

        :param coin: Coin object
        :param explorer_url: string of url of blockchain explorer
        :param user: dict with user information
        :param address: address hash
        :param txs: list of transaction address was involved in
        """
        if not user['rest_url']:
            return

        super(Rest, self).add(coin, explorer_url, user, address, txs)

    def build_message(self, coin, user, address, txs):
        """
        Build dict for notification

        :param coin: Coin object
        :param user: dict with user information
        :param address: address hash
        :param txs: list of transactions
        :return: notification dict
        """
        txs = [list(tx) for tx in txs]
        
        return {
            "address": address,
            "coin": coin,
            "watchlist": user['watchlist_name'],
            "transactions": [[tx[0], tx[2]] for tx in txs], # block number and tx hash
        }

    def send(self):
        """
        Send notifications
        """
        new_queue = []
        while self.queue:
            data = self.queue.pop()
            coin, explorer_url, user, address, txs = data
            payload = self.build_message(coin, user, address, txs)

            try:
                response = requests.post(user['rest_url'], json=payload)
            except requests.exceptions.Timeout:
                new_queue.append(data)
                logger.warn('REST timedout, will be repeated')
            except requests.exceptions.RequestException as e:
                self.queue.append(data)
                logger.warn('REST failed')        
            logger.info('REST sent')

        self.queue = new_queue

