# Cryptoalarm
## Introduction
Cryptocurrencies are becoming popular and the demand for monitoring transactions inside them increases alongside with it. Cryptoalarm
is designed for monitoring transactions involving specific addresses in order to raise alarms. Cryptoalarm scans blockchains of cryptocurrencies such as Bitcoin, Bitcoin Cash, Litecoin, Zcash, Dash, Ethereum and raises alarms about address activities in real-time.

![Demo](https://raw.githubusercontent.com/nesfit/jane-cryptoalarm/master/cryptoalarm-web/laravel/docs/demoalarm.gif)

Requirement for Cryptoalarm was to create an application that allows transac-tions monitoring in multiple cryptocurrencies.Following requirements were specified for an application designated to trans-action monitoring:
* ability  to  monitor  transactions  in  the  wide  spectrum  of  cryptocurrenciesindependently;
* transaction processing in a real-time;
* offer scalability for further extension with new cryptocurrencies;
* process transactions in blocks of the main chain when chain split is detected.

Following  requirements  were  specified  for  a  web  application  designated  towatchlist management:
* multi-user watchlist management;
* address and cryptocurrency specification;
* input/output involvement selection;
* notification type selection;
* notification destination;
* notification email customization.

### JANE Framework
This application is one of the modules of the JANE platform, which offers various mission-specific tools intended for digital forensics of computer networks. JANE follows microservice architecture and offers few containerized modules such as:

* [sMaSheD](https://github.com/kvetak/sMaSheD/) - tracks IP addresses and ports of well-known mining services. It also records the availability of mining service on;
* [Cryptoalarm](https://github.com/nesfit/jane-cryptoalarm/) - sends email/REST notifications triggered by the appearance of cryptocurrency address in new transactions;
* [DeMixer](https://github.com/nesfit/jane-DeMixer/) - DeMixer applies proof-of-concept heuristic (working on BestMixer.io cluster), which can correlate incoming and outgoing transactions going via mixing services;
* [Cryptoclients](https://github.com/nesfit/jane-cryptoclients/) - Blockbook web-application offers generic blockchain explorer supporting major cryptocurrencies (e.g., BTC, ETH, LTS, DASH, ZCASH);
* [Toreator](https://github.com/nesfit/toreator-ui) - stores metadata about Tor relays including IP addresses, capabilities and time when they were active;
* [MozArch](https://github.com/nesfit/mozarch/) - MozArch is web-application that periodically downloads, parses, decodes, and archives (in the MAFF) webpages appearing on the public Internet.

JANE and its modules are outcomes of the [TARZAN project](https://www.fit.vut.cz/research/project/1063/.en) supported by the [Ministry of the Interior of the Czech Republic](https://www.mvcr.cz). Cryptoalarm was developed in the frame of the [master thesis of Lukáš Vokráčko](https://www.vutbr.cz/en/students/final-thesis/detail/114872?zp_id=114872) supervised by [Vladimír Veselý](https://www.fit.vut.cz/person/veselyv/) in 2018.

### Goal
Address monitoring in transactions is the main goal for this module. This type of monitoring can be used by governments, banking institutions or law enforcement agencies to track movements of funds on problematic addresses. Ransomware or malware crypto miner can be used as the examples of these addresses.

Cryptoalarm specializes in systematic transaction monitoring with the focus on extensibility with new cryptocurrencies. Currently, Cryptoalarm supports Bitcoin, Bitcoin Cash, Litecoin, Dash, Zcash and Ethereum. Also, it supports transfers inside ERC20
token systems built on top of Ethereum smart contracts. Zcash allows only monitoring of transaction with transparent addresses (t-addresses). Z-addresses are protected by zero-knowledge proofs, specifically zk-SNARKs.

### Technologies
Cryptoalarm queries official cryptocurrency client (such as Bitcoin Core available as [another JANE module](https://github.com/nesfit/jane-cryptoclients/)) via RPC. 

Cryptoalarm monitoring script written in Pyhton and web application written in PHP with the help of the Laravel framework:

* Python 3
* requests v2.20.0
* psycopg2 v2.8.5
* PostgreSQL 10
* PHP 7.1.3
* Laravel 5.8

## Installation guideline
This section explains reader how to successfully install DeMixer on own infrastructure.

### Install
Cryptoalarm [monitoring script](https://github.com/nesfit/jane-cryptoalarm/tree/master/cryptoalarm-app/python) and [web application](https://github.com/nesfit/jane-cryptoalarm/tree/master/cryptoalarm-web/laravel) source codes are available in separate folders. Deployment of JANE Cryptoalarm module can be cloned via [Git repository](https://github.com/nesfit/jane-cryptoalarm.git).

### Prerequisites
All JANE modules run as containerized microservices. Therefore, the production environment is the same for all of them. JANE uses Docker for containerization. We expect that JANE containers can operate on any containerization solution compatible with Docker (such as Podman).

JANE was developed and tested on CentOS 7/8,  but it can be run on any operating system satisfying the following configuration. Here is a list of installation steps to successfully configure the hosting system:

1. enable routing for (virtual) network interface cards `/sbin/sysctl -w net.ipv4.ip_forward=1`

2. enable NAT on outside facing interfaces `firewall-cmd --zone=public --add-masquerade --permanent
install`

3. add Docker repository 
```
yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo
```

4. install Docker package and its prerequisites `yum install -y docker-ce`

5. run Docker as system service and enable it as one of the daemons 
```
systemctl start docker
systemctl enable docker
``` 

6. install docker-compose staging application 
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.25.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
cp /usr/local/bin/docker-compose /sbin/docker-compose
```

7. install Docker add-on which allows to specify destinations for dynamically created volumes
```
curl -fsSL https://raw.githubusercontent.com/MatchbookLab/local-persist/master/scripts/install.sh | sudo bash
```

### Deployment
Cryptoalarm consists of four containers - Laravel 5.8 web application, nginx 1.10 HTTP server, Python monitoring script, and PostgreSQL database (and optionally adminer for database debugging). In order to deploy Cryptoalarm on your server:

1. clone Cryptoalarm repository `git clone https://github.com/nesfit/jane-cryptoalarm.git`

2. copy container environmental variables file `cp .env.example .env`

3. specify in `.env` container environment variables:
```
POSTGRES_USER=<username>
POSTGRES_PASSWORD=<password>
POSTGRES_DB=<database>
POSTGRES_PORT=<postgres port, should be 5432>
LOCAL_VOLUME_MOUNT_POINT=<mounting point for volumes>
NETWORK=<networkname>
HTTP_PORT=<public http port>
HTTPS_PORT=<public https port>
```
4. copy web application environmental variables file 
`cp ./cryptoalarm-web/config/.env.example ./cryptoalarm-web/config/.env`

5. specify in `./cryptoalarm-web/config/.env` following parameters:
```
DB_HOST=<postgres_host>
DB_PORT=5432
DB_DATABASE=<postgres_db>
DB_USERNAME=<postgres_username>
DB_PASSWORD=<postgres_password>
```
6. copy monitoring script environmental variables file 
`cp ./cryptoalarm-app/python/config.json.example ./cryptoalarm-app/python/config.json`

7. change parameters of monitoring script, which includes PostgreSQL database connection, cryptocurrency clients RPC URLs, mailing server SMTP credentials, and customize notification emails:
```
    "db": "dbname=<database> user=<username> host=<hostname> password=<secret>",
    "coins": [],
    "urls": {
        "BTC": "http://<rpcuser>:<rpcpass>@<hostname/IP>:<rpcport>",
        "LTC": "http://<rpcuser>:<rpcpass>@<hostname/IP>:<rpcport>",
        "DASH":"http://<rpcuser>:<rpcpass>@<hostname/IP>:<rpcport>",
        "BCH": "http://<rpcuser>:<rpcpass>@<hostname/IP>:<rpcport>",
        "ZEC": "http://<rpcuser>:<rpcpass>@<hostname/IP>:<rpcport>",
        "ETH": "http://<rpcuser>:<rpcpass>@<hostname/IP>:<rpcport>"
    },
    "smtp": {
        "server": "<smtpserver>",
        "ssl" : "tls|starttls|none",
        "port": <smtpport>,
        "username": "<smtpusername>",
        "password": "<smtppassword>"
    },
    ...
    "notifier": {
        "server" : "http://<hostname>/",
                "server_prefix_addr" : "/address/",
                "server_prefix_block" : "/block/",
                "server_prefix_tx" : "/tx/",
        "notification_url" : "http://<hostname>/api-endpoint",
        "email_subject" : "[Cryptoalarm] Notification {name}",
        "email_from" : "cryptoalarm@cryptoalarm.tld",
        "email_template" : "<h1>Cryptoalarm {name}</h1>\n<p>triggered for {coin} address {address}</p>\n<p>check fo
llowing transactions</p>\n<p>\n{txs}\n</p>"
```

8. pull [monitoring script](https://hub.docker.com/repository/docker/nesatfit/cryptoalarm-app) and [web app](https://hub.docker.com/repository/docker/nesatfit/cryptoalarm-web) containers from Docker hub repository `docker-compose pull`

9. optionally build monitoring script and web application containers locally `docker-compose build`

10. run containers `docker-compose up -d`

## User manual
Besides console application for address monitoring, we have developed the web application for watchlist management. All these components form the Cryptoalarm, which allows users to set up custom watchlists with a filter for the specific involvement of addresses inside transactions. Cryptoalarm can raise alarms in case of a watched address detection in a transaction. To let users know about such events, alarms can be sent as notifications. Currently, the supported notification types are emails and REST calls.

The purpose of Python monitoring application is to scan blockchains of cryptocurrencies in order to detect new blocks, to process transactions and to send notifications when monitored address is involved in any transaction. The scanning of each cryptocurrency’s blockchain needs to be done in parallel. This is due to the different block times of each cryptocurrency. Those intervals can overlap or new blocks can be generated in approximately at the same time. Transaction processing of one cryptocurrency could become delayed as it would wait until blocks of all other cryptocurrencies were processed in case of serial processing. Also, transaction processing for each cryptocurrency can take significantly different amounts of time. This is caused by each cryptocurrency storing distinct types of information about inputs of transaction. Ethereum can used as an example. Only one RPC call is required to obtain information about transaction inputs. On the other hand, transaction in Bitcoin (and its derivates) requires 1 + 𝑙𝑒𝑛(𝑖𝑛𝑝𝑢𝑡𝑠) RPC calls. This is caused by the process of
identifying senders’ address. 

The main purpose of web application is watchlist management.

### User stories
Cryptoalarm is a combination of monitoring script (which checks occurance of cryptocurrency address within the blockchain and sends notification) and web application that offers user control of the system. Since alarms (in terminology of web all watchlists) have ownership by belonging to some user, the system itself support credentials-based access and user control. It consists of the following views:

* _Dashboard_ - Dashboard consolidates all notifications from all watchlists in a unified timeline.
* _Watchlists_ - This view offers manipulation with watchlists, including creation, editing, and deleting.
* _Notifications_ - Notifications display all alarms belonging to particular cryptocurrency addresses that were raised and recorded by the system. 
* _Login_ - This page is a landing site for unauthorized access through which the user provides session-based credentials.
* _Registration_ - The system is opened so that anyone can freely create an account and set up own alarms.

### Operation
Web application is designed to have multiple screens. The first screen is _Dashboard_ which is designed to be a user’s entry point into the application. It contains a list of notifications about any addresses that user specified watchlist on. This list shows watchlist
name, transaction hash (linking to the blockchain explorer) and notification timestamp.

![dashboard](https://raw.githubusercontent.com/nesfit/jane-cryptoalarm/master/cryptoalarm-web/laravel/docs/dashboard.png)

Another screen is a _Watchlist_. The _Watchlist_ shows all notifications created in according to rules specified in given watchlist. Also, there is a list of identities that match watchlist’s address. Subsequently, there is an overview of rules defined for the given watchlist as cryptocurrency, involvement type (either as input, output or both) and notification type (email, REST or both). Also, there is a preview of a template used to create email notifications. The screen for creating and editing watchlist offers a form to fill all required information.

![watchlist](https://raw.githubusercontent.com/nesfit/jane-cryptoalarm/master/cryptoalarm-web/laravel/docs/watchlist.png)
![createedit](https://raw.githubusercontent.com/nesfit/jane-cryptoalarm/master/cryptoalarm-web/laravel/docs/createupdate.png)

_Notifications_ for a given cryptocurrency address are only subset of all notifications focused on one particular address. 

![notifications](https://raw.githubusercontent.com/nesfit/jane-cryptoalarm/master/cryptoalarm-web/laravel/docs/watchlists.png)


### Testing
To test the performance of Cryptoalarm, we have focused on the speed of transaction processing in the Notifier. We did not measure the performance of interactions with blockchains of cryptocurrencies as it is affected by the connection speed between the application and the node. Interactions with Zcash node running on the same device as Cryptoalarm were almost 4× faster compared to node located on the network with average response time of 15ms. Also, the number of cryptocurrencies supported does not have a significant effect on the performance because Cryptoalarm instance for every cryptocurrency is run in separated thread.

To test the performance of Cryptoalarm, we have measured the average number of transactions in Bitcoin blocks and average number of their inputs and outputs. we have chosen Bitcoin because it is currently the most used cryptocurrency. There are 20 730 000 transactions in the last 10 000 Bitcoin blocks. The average number of transactions per block equals to 2073. Those transactions have on average 2.577 inputs and 2.398 outputs. For the testing purposes, we have adjusted these numbers to 2.5 inputs and 2.5 outputs per transaction. 

To the measure performance, we have created scenarios with: 10, 100, 1000, 5000 and 10000 watchlists. Then, for every scenario, we have created 2073 transactions with the average of 2.5 inputs and 2.5 outputs. Those transactions were generated artificially to have the occurrence of watched address of: 10%, 25%, 50%, and 75%.

We have measure the performance in two separated phases. First phase covers processing transactions and storing this information inside Cryptoalarm. The results are shown on following figure. As you can see the number of watchlists has major impact on performance. Percentage of watched address occurrence has only minor impact.

![Phase1](https://raw.githubusercontent.com/nesfit/jane-cryptoalarm/master/cryptoalarm-web/laravel/docs/t1.png)

Second phase consists of generating notifications for transactions matching watchlists. The results are shown on the next figure. The number of occurrences of watched addresses had more impact on notification times in comparison to processing time. This is due to the number of notifications that needs to be generated and saved in the database.

![Phase2](https://raw.githubusercontent.com/nesfit/jane-cryptoalarm/master/cryptoalarm-web/laravel/docs/t2.png)

## Programmer's documentation
The programmer's documentation for Cryptoalarm is autogenerated with the help of phpDox and pydoc. This documentation is available statically in `docs` [folder](https://github.com/nesfit/jane-cryptoalarm/tree/master/demixer/docs). Moreover, for your convenience, it is also available online through JANE's [landing page](https://github.com/nesfit/jane-splashscreen/):

* [for web application](https://jane.nesad.fit.vutbr.cz/docs/cryptoalarm/web/index.xhtml)
* [for monitoring script](https://jane.nesad.fit.vutbr.cz/docs/cryptoalarm/app/cryptoalarm.html)

### Class Diagram
Class diagram corresponding to Python monitoring script of final application:

![Class diagram](https://raw.githubusercontent.com/nesfit/jane-cryptoalarm/master/cryptoalarm-web/laravel/docs/cd.png)

Both monitoring script and web application synchronizes themselves via PostgreSQL database. Here is the Entity reliationship diagram of database scheme:

![ER](https://raw.githubusercontent.com/nesfit/jane-cryptoalarm/master/cryptoalarm-web/laravel/docs/er.png)
