''' This module will build our database object. '''
import pymysql


class Database():
    def __init__(self, ip, user, password, database):
        self.IP = ip
        self.USER = user
        self.DB_PASS = password
        self.DATABASE = database

    def credntial_check(self, email, password):
        credentials = False
        sql = ('SELECT * FROM  users WHERE  email="'+email+'"')
        row = self.query('PULL', sql)
        if(len(row) != 0 and row[0][1] == email and row[0][2] == password):
            credentials = True
        return (credentials)

    def register(self, first, last, uType, vKey, email, password):
        arg = (0, email, password, uType)
        sql = "INSERT INTO users (user_id, email, password, role) VALUES (%s, %s, %s, %s)"
        print(arg)
        self.query('PUSH', sql, arg)
        print("PULL", "Select * from users")

    def connect(self):
        db = pymysql.connect(host=(self.IP), user=self.USER,
                             password=self.DB_PASS, db=self.DATABASE)
        cursor = db.cursor()
        return (db, cursor)

    def query(self, qType, statement, *args):
        database, cursor = self.connect()
        cursor.execute(statement, *args)
        row = cursor.fetchall()
        if(qType == 'PULL'):
            return(row)
        else:
            database.commit()
        database.close()
