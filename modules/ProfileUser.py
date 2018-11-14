from modules import Database
from hashlib import md5
import os

IP = '35.221.39.35'  # InternREQ Official DB | GearGrinders
PASS = os.environ.get('DB_PASS')
db = Database.Database(IP, 'root', PASS, 'internreq')


class ProfileUser():
    def __init__(self, user_id):
        sql = 'SELECT * FROM users WHERE user_id = "%s"' % (user_id)
        row = db.query('PULL', sql)[0]
        self.email = row[1]
        # avatar by Gravatar
        self.avatar_s, self.avatar_m, self.avatar_l = self.picLoader(
            self.email)
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

        # additional datapoints
        if (self.role == 'student'):
            self.grad_date = row[14]
            self.gpa = row[15]

    def picLoader(self, email):
        digest = md5(email.lower().encode('utf-8')).hexdigest()
        # 36px square
        avatar_s = 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, 36)
        # 80px square
        avatar_m = 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, 80)
        # 128px square
        avatar_l = 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, 128)
        return(avatar_s, avatar_m, avatar_l)
