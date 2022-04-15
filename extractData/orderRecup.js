var Datastore = require('nedb')
const fs = require('fs')
const db1 = new Datastore({filename: '../app/database.db', autoload: true})
db1.loadDatabase(err => {
    if (err) console.log('Error Database Orders:', err); 
    else console.log('MongoDB Orders OK!');
});

// Thi file able us to read nedb data. Nedb is a datastore which only js can read or write. 
// We read the database and write in txt file with ; splitter
db1.find({}, function (err, docs) {
  docs.forEach(element => {
    content = ''
    content += element.ballCoord + ';'
    content += element.redCoords + ';'
    content += element.blueCoords + ';'
    content += element.score + ';'
    content += element.actualPlayer + ';'
    content += element.team + ';'
    content += element.order + '\n'
    fs.writeFile('order.txt', content,{ flag: 'a+' }, err => {
        if (err) {
          console.error(err)
          return
        }
        //file written successfully
    })
  });
});