'use strict';

require('dotenv').config()

var fs        = require('fs');
const express = require('express');
var path      = require("path");
var cors      = require('cors');
const Datastore = require('nedb');
//const spawn = require('await-spawn');
const orderDB = require("./db.js");
const UserDB = require("./dataUser.js");
const celery = require('celery-node');

const bcrypt = require('bcrypt')
const passport = require('passport')
const flash = require('express-flash')
const session = require('express-session')
const methodOverride = require('method-override')

const initializePassport = require('./passport-config')

const app = express();
app.use(cors());

app.use("/dist", express.static(path.join(__dirname, "dist/")));
app.use("/public",   express.static(path.join(__dirname, "webapp/public/")));
app.use("/logsGames",   express.static(path.join(__dirname, "../logsGames/")));

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

console.log('Loading MongoDB Users ...');
const db2 = new Datastore({filename: './users.db', autoload: true})
db2.loadDatabase(err => {
    if (err) console.log('Error Database Users:', err); 
    else console.log('MongoDB Users OK!');
});

const usersDB = new UserDB.default(db2)

// initializePassport(
//   passport,
//   email => users.find(user => user.email == email),
//   id => users.find(user => user.id === id)
// )

initializePassport(
  passport,
  email => usersDB.getUserByEmail(email),
  id => usersDB.getUserByid(id)
)

app.set('view-engine', 'ejs')
app.use(express.urlencoded({ extended: false }))
app.use(flash())
app.use(session({
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false
}))
app.use(passport.initialize())
app.use(passport.session())
app.use(methodOverride('_method'))

app.get('/login', checkNotAuthenticated, (req, res) => {
  res.render('login.ejs')
})

app.post('/login', checkNotAuthenticated, passport.authenticate('local', {
  successRedirect: '/game',
  failureRedirect: '/login',
  failureFlash: true
}))

app.get('/register', checkNotAuthenticated, (req, res) => {
  res.render('register.ejs')
})

app.post('/register', checkNotAuthenticated, async (req, res) => {
  try {
    const hashedPassword = await bcrypt.hash(req.body.password, 10)

    usersDB.createUser(req.body.name, req.body.email, hashedPassword)
    res.redirect('/login')
  } catch {
    res.redirect('/register')
  }
})

app.delete('/logout', (req, res) => {
  req.logOut()
  res.redirect('/login')
})

function checkAuthenticated(req, res, next) {
  if (req.isAuthenticated()) {
    return next()
  }

  res.redirect('/login')
}

function checkNotAuthenticated(req, res, next) {
  if (req.isAuthenticated()) {
    return res.redirect('/')
  }
  next()
}

function Producer(req, res) {
  let client = celery.createClient(
    "amqp://localhost:5672",
    "amqp://localhost:5672",
    "celery"
  );

  let task = client.createTask("simple_example.create_match");
  console.log(task)
  let result = task.applyAsync();
  console.log(result)
  result.get().then(data => {
    console.log("Result producer : " + data);
    client.disconnect();
  })
}

app.get('/', (req, res) => {
  res.sendFile(get_path("home.html"));
});
app.get('/game', checkAuthenticated, (req, res) => {
  res.sendFile(get_path("index.html"));
});
app.get('/rules', (req, res) => {
  res.sendFile(get_path("rules.html"));
});

app.get('/create', checkAuthenticated, (req, res) => {
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

console.log('Loading MongoDB Orders ...');
const db1 = new Datastore({filename: './database.db', autoload: true})
db1.loadDatabase(err => {
    if (err) console.log('Error Database Orders:', err); 
    else console.log('MongoDB Orders OK!');
});


const ordersDB = new orderDB.default(db1)

app.use(express.json())


app
  .route("/db")
  .get((req, res) => {
    const data = ordersDB.recupData()
    .then((data) => {
      console.log(data)
    })
    .catch((err) => res.status(500).send(err));
  })
  .post( async (req,res) => {
    console.log(req.body)
    const {ballCoord, redCoords, blueCoords, score, actualPlayer, order} = req.body
    try {
    const data = ordersDB.insertData(ballCoord, redCoords, blueCoords, score, actualPlayer, order)
      if (!data){
          res.status(404).send({"status": "error", "msg": "Error to put data retry"});
      }else
          res.status(201).send({"msg": "Data insert in orderDB"})
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

