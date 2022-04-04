# FootballGame-ML

## Start

For now, the project is only usable in a Linux environment.
We are looking for solutions on how to make the project usable on macOS and Windows.

To start the web server, you need to use the following commmand while in the **/app** folder : 
```
npm run start
```

Note - NodeJS is needed in order to make the project runnable. If needed, you can install NodeJS at the following address :
```
https://nodejs.org/en/download/
```

Also you need to start RabbitMQ for Celery (to install RabbitMQ : https://www.rabbitmq.com/download.html):
```
sudo systemctl enable rabbitmq-server
sudo systemctl start rabbitmq-server
```
To check if rabbitmq started well (status : running)
```
sudo systemctl status rabbitmq-server
```
With **erlang** you can go on localhost:15672 to open the RabbitMQ Management

Now you can run Celery server:
```
celery -A <File-Contain-Celery-App> worker -l info
```

## Datasets structures

2 Datasets:
 - Users
 - Orders

### Users

This dataset (MongoDB) records all party IDs for each of the users.

For each element:
 - name
 - email
 - password
 - iDlogs : lists of all party IDs
 - id : Generate by MongoDB
  
### Orders

The MongoDB dataset registers all orders from all the players.

For each element:
- userID 
- ballCoord
- redCoords : Position x  Position y for all red players
- blueCoords : Position x  Position y for all red players
- score
- ActualPlayer : The position of the player who the order is destinate
- order
- id : Generate by MongoDB

### Membres du binôme
  - KRISNI Almehdi
  - ARICHANDRA Santhos

### Lien vers le document de suivi
https://docs.google.com/document/d/1euuWMVE371zk5M_5zQL6HjjZD1EbQyiXrzJFteEHmKI/edit?usp=sharing
