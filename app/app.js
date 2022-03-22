'use strict';

var fs        = require('fs');
const express = require('express');
var path      = require("path");
var cors      = require('cors');
const Datastore = require('nedb');
const DB = require("./db.js");


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

app.get('/', (req, res) => {
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

// Connection with the Mongo Database
// mongoose
// .connect('mongodb+srv://admin:jG32gSdMFIaGrF97@football.jt6fw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
// .then(() => {
//   console.log('DataBase Connected')
// })
// .catch(error => {
//   console.log('DataBase not Connected' + error)
// })

console.log('Loading MongoDB...');
const db = new Datastore({filename: './database.db', autoload: true})
db.loadDatabase(err => {
    if (err) console.log('Error Database:', err); 
    else console.log('MongoDB OK!');
});

const db2 = new DB.default(db)
// router.use(express.json());
// router.use((req, res, next) => {
//     console.log('API: method %s, path %s', req.method, req.path);
//     console.log('Body', req.body);
//     next();
// });

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
    // const data = db2.insertData(ballCoord, redCoords, blueCoords, score, actualPlayer, order)
    // .then(() => res.status(201).send(data))
    // .catch((err) => res.status(500).send(err));
  })

// router.post('/', function(req, res) {
//     // do something w/ req.body or req.files 
// });
// const db2 = new DB.default(db);
// // Insert the order and all positions in database
// router.put("/insertData", async (req, res) => {
//   const data = db2.insertMsg(req.body)
//   .then(() => res.status(201).send(data))
//   .catch((err) => res.status(500).send(err));
// })
// // Get data to verify if route works
// router.post("/recupData", async (req, res) => {
//   const data = db2.recupData()
//   .then(() => res.status(201).send(data))
//   .catch((err) => res.status(500).send(err));
// })

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`App listening on http://localhost:${PORT}`);
  console.log('Press Ctrl+C to quit.');
});

