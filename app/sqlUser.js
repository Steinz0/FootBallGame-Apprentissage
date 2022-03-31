class Users {
    constructor(users) {
        this.users = users
        const createUserTable = `CREATE TABLE IF NOT EXISTS users (
            name VARCHAR(50) NOT NULL,
            email VARCHAR(50) NOT NULL PRIMARY KEY,
            password VARCHAR(50) NOT NULL
        )`;
        this.users.exec(createUserTable, err => {
            if (err) throw err;
            console.log('SQLite3 User ready');
        });
    }

    create(name, email, password) {
        return new Promise((resolve, reject) => {
            const insertUser = `INSERT INTO users
            VALUES ( '${name}', '${email}', '${password}')`;

            this.users.exec(insertUser, err => {
                if (err) reject(err);
                else resolve(email);
            })
        })
    }

    getUserByEmail(email){
        return new Promise((resolve, reject) => {
            const getUserByE = `SELECT  * FROM users WHERE email="${email}"`;
            this.users.get(getUserByE, (err, res) => {
                if(err) {
                    reject(err);
                } else {
                    resolve(res);
                }
            })
        }) 
    }

    getUserByid(id){
        return new Promise((resolve, reject) => {
            const getUserByE = `SELECT ROWID, * FROM users WHERE ROWID="${id}"`;
            this.users.get(getUserByE, (err, res) => {
                if(err) {
                    reject(err);
                } else {
                    resolve(res);
                }
            })
        }) 
    }

    getAll(){
        return new Promise((resolve, reject) => {
            const getUsers = `SELECT ROWID, * FROM users`;
            this.users.get(getUsers, (err, res) => {
                if(err) {
                    reject(err);
                } else {
                    resolve(res);
                }
            })
        }) 
    }
}

exports.default = Users;