''' This module will build our database object. '''
import pymysql
import hashlib


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
        if(len(row) != 0 and row[0][1] == email and row[0][2] == self.encrypt(password)):
            credentials = True
        return (credentials)

    def register(self, first, last, uType, vKey, email, password):
        password = self.encrypt(password)
        arg = (0, email, password, uType)
        sql = "INSERT INTO users (user_id, email, password, role) VALUES (%s, %s, %s, %s)"
        self.query('PUSH', sql, arg)

    def connect(self):
        db = pymysql.connect(host=(self.IP), user=self.USER,
                             password=self.DB_PASS, db=self.DATABASE)
        cursor = db.cursor()
        return (db, cursor)

    def encrypt(self, toEncrypt):
        sha = hashlib.sha256()
        sha.update(toEncrypt.encode('utf-8'))
        encrypted = sha.hexdigest()
        return encrypted

    '''
    The query function will be the bread and butter of our database object
    
    arguments:
        self: required for object construction
        qType: short for query type. This will tell the databse if you are pulling ("PULL") down data 
            to work with, (i.e logging in) or pushing ("PUSH") data to the database (i.e registration)
        statment: the SQL statment to be run
        *args: variable amout of arguments to be appended to the statment (i.e.: when inserting via pymysql) 

    return:
        if pulling down data it returns a tuple that was gained via your query
        if pushing data there is no return
    '''

    def query(self, qType, statement, *args):
        database, cursor = self.connect()
        cursor.execute(statement, *args)
        row = cursor.fetchall()
        if(qType == 'PULL'):
            return(row)
        else:
            database.commit()
        database.close()
