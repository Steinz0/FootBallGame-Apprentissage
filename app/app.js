'use strict';

var fs        = require('fs');
const express = require('express');
var path      = require("path");
var cors      = require('cors');
const Datastore = require('nedb');
const spawn = require('await-spawn');
const DB = require("./db.js");
const celery = require('celery-node');

const client = celery.createClient(
  "amqp://",
  "amqp://",
  "match_tasks"
);

function Producer(req, res) {
  const task = client.createTask("Exemple_GIT_REPO.simple_example.print_hello");
  const result = task.applyAsync();
  result.get().then(data => {
    console.log("Result producer : " + data);
    client.disconnect();
  })
}

async function callPython(req, res) {
    let process = await spawn('python',["../gameEngine/Exemple_GIT_REPO/simple_example.py"] );
    console.log(process.toString())

    let filename = Math.random() * 100000000000;
    fs.writeFile('../logsGames/' + filename + '.txt', process.toString(), { flag: 'a+' }, err => {
      if (err) {
        console.error(err);
        return;
      }
      //file written successfully
    });
}

function fromDir(startPath,filter){
  var files_list = [];
  var files=fs.readdirSync(startPath);
  for(var i=0;i<files.length;i++){
      var filename=path.join(startPath,files[i]);
      var stat = fs.lstatSync(filename);
      if (filename.indexOf(filter)>=0) {
          files_list.push(filename);
      };
  };
  return files_list;
}

function get_path(file){
  return path.join(path.join(__dirname, "webapp/"), file);
}

const app = express();
app.use(cors());

app.use("/dist", express.static(path.join(__dirname, "dist/")));
app.use("/public",   express.static(path.join(__dirname, "webapp/public/")));
app.use("/logsGames",   express.static(path.join(__dirname, "../logsGames/")));


app.get('/', (req, res) => {
  res.sendFile(get_path("home.html"));
});
app.get('/game', (req, res) => {
  res.sendFile(get_path("index.html"));
});
app.get('/rules', (req, res) => {
  res.sendFile(get_path("rules.html"));
});

app.get('/create', (req, res) => {
  Producer();
  res.sendFile(get_path("index.html"));
});

/**
 * Create all HTML routes
 * **/
const files = fromDir(path.join(__dirname, "webapp/"),'.html');
files.forEach(file => {
  let route = file.split("/");
  route = route[route.length - 1];

  console.log("Open route:", route, file);
  app.get('/'+route, (req, res) => {
    res.sendFile(file);
  });
});

console.log('Loading MongoDB...');
const db = new Datastore({filename: './database.db', autoload: true})
db.loadDatabase(err => {
    if (err) console.log('Error Database:', err); 
    else console.log('MongoDB OK!');
});

const db2 = new DB.default(db)

app.use(express.json())
app
  .route("/db")
  .get((req, res) => {
    const data = db2.recupData()
    .then((data) => {
      console.log(data)
    })
    .catch((err) => res.status(500).send(err));
  })
  .post( async (req,res) => {
    console.log(req.body)
    const {ballCoord, redCoords, blueCoords, score, actualPlayer, order} = req.body
    try {
    const data = db2.insertData(ballCoord, redCoords, blueCoords, score, actualPlayer, order)
      if (!data){
          res.status(404).send({"status": "error", "msg": "Error to put data retry"});
      }else
          res.status(201).send({"msg": "Data insert in DB"})
    }
    catch(e) {
      res.send(e);
    }
  })

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`App listening on http://localhost:${PORT}`);
  console.log('Press Ctrl+C to quit.');
});

