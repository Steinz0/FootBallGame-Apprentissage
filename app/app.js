'use strict';

var fs        = require('fs');
const express = require('express');
var path      = require("path");
var cors      = require('cors');
const Datastore = require('nedb');
const DB = require("./db.js");
let file_content = ''

function callName(req, res) {
      
    // Use child_process.spawn method from 
    // child_process module and assign it
    // to variable spawn
    var spawn = require("child_process").spawn;
      
    // Parameters passed in spawn -
    // 1. type_of_script
    // 2. list containing Path of the script
    //    and arguments for the script 
      
    // E.g : http://localhost:3000/name?firstname=Mike&lastname=Will
    // so, first name = Mike and last name = Will
    var process = spawn('python',["../gameEngine/Exemple_GIT_REPO/simple_example.py"] );
  
    // Takes stdout data from script which executed
    // with arguments and send this data to res object
    process.stdout.on('data', function(data) {
        res.send(data.toString());
        file_content = data.toString()
        console.log(file_content)

        fs.writeFile('../logsGames/test.txt', file_content, err => {
          if (err) {
            console.error(err)
            return
          }
          //file written successfully
        })
    } )
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

app.get('/name', callName);

app.get('/', (req, res) => {
  res.sendFile(get_path("home.html"));
});
app.get('/game', (req, res) => {
  res.sendFile(get_path("index.html"));
});
app.get('/rules', (req, res) => {
  res.sendFile(get_path("rules.html"));
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

