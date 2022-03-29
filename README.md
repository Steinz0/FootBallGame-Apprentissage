# FootballGame-ML

## Start the server

To start the web server, you just need to start this commmand on the app folder: 
```
npm run dev
```
## Datasets structures

2 Datasets:
 - Users
 - Orders

### Users

MongoDB again, this dataset registre all logs games for all user.

For each element:
 - userId
 - logs : lists of all log ids

### Logs Games

MongoDB again, this dataset registre all order for all user.

For each element:
- userId 
- ballCoord
- redCoords : Position x  Position y for all red players
- blueCoords : Position x  Position y for all red players
- score
- ActualPlayer : The position of the player you the order is destinate
- order

### Membres du binôme
  - KRISNI Almehdi
  - ARICHANDRA Santhos

### Lien vers le document de suivi
https://docs.google.com/document/d/1euuWMVE371zk5M_5zQL6HjjZD1EbQyiXrzJFteEHmKI/edit?usp=sharing
