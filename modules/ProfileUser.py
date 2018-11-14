from modules import Database
from hashlib import md5
import os

'''
# Database Connect
IP = '35.221.39.35'  # InternREQ Official DB | GearGrinders
PASS = os.environ.get('DB_PASS')
db = Database.Database(IP, 'root', PASS, 'internreq')
'''

# Database Access
# <!> Set the environment variable before testing locally
# (ie. 'export DB_PASS=ourpassword'   or  'set DB_PASS=ourpassword')
db_user = 'root'
db_ip = '35.221.39.35'
db_name = 'internreq'
db_password = os.environ.get('DB_PASS')
db_connection_name = 'birmingham4test:us-east4:internreq-1'

# When deployed to App Engine, the `GAE_ENV` environment variable will be
# set to `standard`
if os.environ.get('GAE_ENV') == 'standard':
    # If deployed, use the local socket interface for accessing Cloud SQL
    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    engine_url = 'mysql+pymysql://{}:{}@/{}?unix_socket={}'.format(
        db_user, db_password, db_name, unix_socket)
else:
    # If running locally, use the TCP connections instead
    # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
    # so that your application can use 127.0.0.1:3306 to connect to your
    # Cloud SQL instance
    host = '127.0.0.1'
    engine_url = 'mysql+pymysql://{}:{}@{}/{}'.format(
        db_user, db_password, host, db_name)

db = Database.Database(engine_url)

class ProfileUser():
    def __init__(self, user_id):
        sql = 'SELECT * FROM users WHERE user_id = "%s"' % (user_id)
        row = db.query('PULL', sql)[0]
        self.email = row[1]
        self.role = row[3]
        sql = 'SELECT * FROM %s WHERE user_id = "%s"' % (self.role, user_id)
        row = db.query('PULL', sql)[0]
        self.fname = row[1]
        self.lname = row[2]
        self.full_name = row[1]+' '+row[2]
        self.title = row[3]
        self.department = row[4]
        self.major = row[4]
        self.company = row[4]
        self.location = row[5]
        self.about = row[6]
        self.url = row[7]
        self.email = row[8]
        self.phone = row[9]
        self.phone_desc = row[10]
        self.verified = row[11]
        self.education = row[12]
        self.additional = row[13]
        # avatar by Gravatar
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        # 36px square
        self.avatar_s = 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, 36)
        # 80px square
        self.avatar_m = 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, 80)
        # 128px square
        self.avatar_l = 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, 128)

        # additional datapoints
        if (self.role == 'student'):
            self.grad_date = row[14]
            self.gpa = row[15]
