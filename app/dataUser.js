class UserDB{
    constructor(db) {
        this.db = db
        this.db.loadDatabase();
    };

    createUser(name, email, password) {
        return new Promise((resolve, reject) => {
            this.db.insert({name, email, password}, function(err, result) {
                if (err) {
                    reject(err);
                }else{
                    resolve(result);
                }
            });
        })
    }

    getUserByEmail(email){
        return new Promise((resolve, reject) => {
            this.db.find({email: email}).exec( function (err, result) {
                if (err){
                    reject(err);
                }
                resolve(result);
            });
        }) 
    }

    getUserByid(id){
        return new Promise((resolve, reject) => {
            this.db.find({_id: id}).exec( function (err, result) {
                if (err){
                    reject(err);
                }
                resolve(result);
            });
        }) 
    }
}


exports.default = UserDB;