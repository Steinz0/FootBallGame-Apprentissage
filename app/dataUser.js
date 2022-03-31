class UserDB{
    constructor(db) {
        this.db = db
        this.db.loadDatabase();
    };

    createUser(name, email, password) {
        return new Promise((resolve, reject) => {
            let idMatches = []
            this.db.insert({name, email, password, idMatches}, function(err, result) {
                if (err) {
                    reject(err);
                }else{
                    resolve(result);
                }
            });
        })
    }

    async addMatch(email, idMatch) {
        const user = await this.getUserByEmail(email)
        let listMatches = user[0].idMatches
        listMatches.push(idMatch)
        return new Promise((resolve, reject) => {
            this.db.update({ email: email}, { $set: {idMatches: listMatches}}, function (err, numReplaced) {
            if (err){
                reject(err)
            } else {
                resolve(numReplaced)
            }
            })
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