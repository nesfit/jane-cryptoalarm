# Cryptoalarm
## Introduction
Cryptocurrencies are becoming popular and the demand for monitoring transactions inside them increases alongside with it. Cryptoalarm
is designed for monitoring transactions involving specific addresses in order to raise alarms. Cryptoalarm scans blockchains of cryptocurrencies such as Bitcoin, Bitcoin Cash, Litecoin, Zcash, Dash, Ethereum and raises alarms about address activities in real-time.

![Demo]()

### JANE Framework
This application is one of the modules of the JANE platform, which offers various mission-specific tools intended for digital forensics of computer networks. JANE follows microservice architecture and offers few containerized modules such as:

* [sMaSheD](https://github.com/kvetak/sMaSheD/) - tracks IP addresses and ports of well-known mining services. It also records the availability of mining service on;
* [Cryptoalarm](https://github.com/nesfit/jane-cryptoalarm/) - sends email/REST notifications triggered by the appearance of cryptocurrency address in new transactions;
* [DeMixer](https://github.com/nesfit/jane-DeMixer/) - DeMixer applies proof-of-concept heuristic (working on BestMixer.io cluster), which can correlate incoming and outgoing transactions going via mixing services;
* [Cryptoclients](https://github.com/nesfit/jane-cryptoclients/) - Blockbook web-application offers generic blockchain explorer supporting major cryptocurrencies (e.g., BTC, ETH, LTS, DASH, ZCASH);
* [Toreator](https://github.com/nesfit/toreator-ui) - stores metadata about Tor relays including IP addresses, capabilities and time when they were active;
* [MozArch](https://github.com/nesfit/mozarch/) - MozArch is web-application that periodically downloads, parses, decodes, and archives (in the MAFF) webpages appearing on the public Internet.

JANE and its modules are outcomes of the [TARZAN project](https://www.fit.vut.cz/research/project/1063/.en) supported by the [Ministry of the Interior of the Czech Republic](https://www.mvcr.cz). Coin DeMixer was developed in the frame of the [master thesis of Lukáš Vokráčko](https://www.vutbr.cz/en/students/final-thesis/detail/114872?zp_id=114872) supervised by [Vladimír Veselý](https://www.fit.vut.cz/person/veselyv/) in 2018.

### Goal
Address monitoring in transactions is the main goal for this project. This type of monitoring can be used by governments, banking institutions or law enforcement agencies to track movements of funds on problematic addresses. Ransomware or malware crypto miner can be used as the examples of these addresses.

Cryptoalarm specializes in systematic transaction monitoring with the focus on extensibility with new cryptocurrencies. Currently, Cryptoalarm supports Bitcoin, Bitcoin Cash, Litecoin, Dash, Zcash and Ethereum. Also, it supports transfers inside ERC20
token systems built on top of Ethereum smart contracts. Zcash allows only monitoring of transaction with transparent addresses (t-addresses). Z-addresses are protected by zero-knowledge proofs, specifically zk-SNARKs.

### Technologies
Cryptoalarm queries official cryptocurrency client (such as Bitcoin Core available as [another JANE module](https://github.com/nesfit/jane-cryptoclients/)) via RPC. 

Cryptoalarm parsing script written in Pyhton and web application written in PHP with the help of the Laravel framework:

* Python 3
* requests v2.20.0
* psycopg2 v2.8.5
* PostgreSQL 10
* PHP 7.1.3
* Laravel 5.8

## Installation guideline
Coin DeMixer web application source codes are available in the followin [GitHub repository folder](https://github.com/nesfit/jane-DeMixer/tree/master/demixer). Deployment of JANE DeMixer module can be cloned via [Git repository](https://github.com/nesfit/jane-DeMixer.git).

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
Coin DeMixer consists of two containers - Laravel 5.8 web application and nginx 1.10 HTTP server. In order to deploy DeMixer on your server:

1. clone DeMixer repository `git clone https://github.com/nesfit/jane-DeMixer.git`

2. copy container environmental variables file `cp .env.example .env`

3. specify in `.env` public port on which DeMixer will be available and existing virtual network name nano .env
```
NETWORK=<docker_network>
HTTP_PORT=<public_port>
```
4. copy web application environmental variables file 
`cp ./demixer/.env.example ./demixer/.env`

5. specify in `./demixer/.env` following parameters (where for Bitcoin/Litecoin clients you may consider to deploy JANE [cryptoclients module](https://github.com/nesfit/jane-cryptoclients/))
```
CLUSTER_CLIENT=<DeMixer compatible cluster provider>
BTC_CORE_HOSTNAME=<host running official Bitcoin client>
BTC_CORE_PORT=<port for RPC calls>
BTC_CORE_USERNAME=<Bitcoin client RPC username>
BTC_CORE_PASSWORD=<Bitcoin client RPC password>
LTC_CORE_HOSTNAME=<host running official Litecoin client>
LTC_CORE_PORT=<port for RPC calls>
LTC_CORE_USERNAME=<Litecoin client RPC username>
LTC_CORE_PASSWORD=<Litecoin client RPC password>
```
6. pull containers from [Docker hub repository](https://hub.docker.com/repository/docker/nesatfit/demix-app) `docker-compose pull`

7. optionally build web application locally `docker-compose build demix-app`

8. run containers `docker-compose up -d`

## User manual
Besides console application for address monitoring, we have developed the web application for watchlist management. All these components form the Cryptoalarm, which allows users to set up custom watchlists with a filter for the specific involvement of addresses inside transactions. Cryptoalarm can raise alarms in case of a watched address detection in a transaction. To let users know about such events, alarms can be sent as notifications. Currently, the supported notification types are emails and REST calls.

### User stories

### Operation


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
* [for web application](https://jane.nesad.fit.vutbr.cz/docs/cryptoalarm/app/cryptoalarm.html)

### Class Diagram
Class diagram corresponding to Python parsing script of final application:

![Class diagram](https://raw.githubusercontent.com/nesfit/jane-cryptoalarm/master/cryptoalarm-web/laravel/docs/cd.png)

Both parsing script and web application synchronizes themselves via PostgreSQL database. Here is the Entity reliationship diagram of database scheme:

![ER](https://raw.githubusercontent.com/nesfit/jane-cryptoalarm/master/cryptoalarm-web/laravel/docs/er.png)
