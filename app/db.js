class DB{
    constructor(db) {
        this.db = db
        this.db.loadDatabase();
    };

    insertData(ballCoord, redCoords, blueCoords, score, actualPlayer, order) {
        return new Promise((resolve, reject) => {
            this.db.insert({ballCoord, redCoords, blueCoords, score, actualPlayer, order}, function(err, result) {
                if (err) {
                    console.log("KO")
                    reject(err);
                }else{
                    console.log("OK")
                    resolve(result);
                }
            });
        })
    }

    recupData(){
        return new Promise((resolve, reject) => {
            this.db.find({}).exec( function (err, result) {
                if (err){
                    reject(err);
                }
                resolve(result.reverse());
            });
        }) 
    }
}


exports.default = DB;