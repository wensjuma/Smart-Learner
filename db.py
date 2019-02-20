from flask_mysqldb import MySQLdb

class Database:
    def __init__(self):
        host = "127.0.0.1"
        user = "root"
        password = ""
        db = "Msomi"
        self.con = MySQLdb.connect(host = host, user = user, password = password, db = db, 
        cursorclass = MySQLdb.cursors.DictCursor)
        self.cur = self.con.cursor()

    def list_users(self):
        self.cur.execute("SELECT * FROM users LIMIT 50")
        result = self.cur.fetchall()
        return result