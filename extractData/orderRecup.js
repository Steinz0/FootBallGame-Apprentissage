var Datastore = require('nedb')
const fs = require('fs')
const db1 = new Datastore({filename: '../app/Data/database.db', autoload: true})
db1.loadDatabase(err => {
    if (err) console.log('Error Database Orders:', err); 
    else getFeatures();
});

// This file able us to read nedb data. Nedb is a datastore which only js can read or write. 
// We read the database and write in txt file with ; splitter

function getFeatures(){
  db1.find({}, function (err, docs) {
    content = ''
    docs.forEach(element => {
      content += element.ballCoord + ';'
      content += element.redCoords + ';'
      content += element.blueCoords + ';'
      content += element.score + ';'
      content += element.actualPlayer + ';'
      content += element.team + ';'
      content += element.order + '\n'
    });
    fs.writeFile('order.txt', content,{ flag: 'w+' }, err => {
        if (err) {
          console.error(err)
          return 
        }
        //file written successfully
    })
  });
}