# Football-Apprentissage

### Start the server

To start the web server, you just need to start this commmand on the app folder: 
```
npm run dev
```
### Datasets structures

2 Datasets:
 - Users
 - Logs Games

#### Users

It's a MongoDb dataset, which you have the userid and a list of all logs ids for the the userid

#### Logs Games

The file represents the positions of the players and the ball in the current match.

How to read one line :
- 1st value : Red Team Score
- 2nd value : Blue Team Score
- 3rd value : Position x to the ball
- 4th value : Position y to the ball
- [Nb of red players] : Position x  Position y
- [Nb of blue players] : Position x  Position y

### Membres du binôme
  - KRISNI Almehdi
  - ARICHANDRA Santhos

### Lien vers le document de suivi
https://docs.google.com/document/d/1euuWMVE371zk5M_5zQL6HjjZD1EbQyiXrzJFteEHmKI/edit?usp=sharing
