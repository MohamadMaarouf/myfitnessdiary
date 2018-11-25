''' This module will build our database object. '''
import sqlalchemy
import hashlib


class Database():
    def __init__(self, url, pool_size=3):
        self.URL = url
        self.engine = sqlalchemy.create_engine(url, pool_size=pool_size)

    def credntial_check(self, email, password):
        credentials = False
        sql = "SELECT * FROM  users WHERE email LIKE '%s'" % email
        row = self.query('PULL', sql)
        if(len(row) != 0 and row[0][1] == email and row[0][2] == self.encrypt(password)):
            credentials = True
        return (credentials)

    def register(self, first, last, uType, email, password):
        password = self.encrypt(password)
        arg = (0, email, password, uType)
        sql = "INSERT INTO users (user_id, email, password, role) VALUES (%s, %s, %s, %s)"
        self.query('PUSH', sql, arg)

    def connect(self):
        # The Engine object returned by create_engine() has a QueuePool integrated
        # See https://docs.sqlalchemy.org/en/latest/core/pooling.html for more
        # information
        engine = sqlalchemy.create_engine(self.URL, pool_size=3)
        return (engine)

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
        connection = self.engine.connect()
        cursor = connection.execute(statement, *args)
        result = cursor.fetchall()

        # If the connection comes from a pool, close() will send the connection
        # back to the pool instead of closing it
        connection.close()

        if(qType.capitalize() == 'Pull'):
            return(result)
