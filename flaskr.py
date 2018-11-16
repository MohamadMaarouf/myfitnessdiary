''' Flask server to handle routing for InternREQ.com. '''

# Import's
from modules import forms, Database
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_mail import Mail
from flask_mail import Message
# Flask-Login attempt import's
from werkzeug.security import generate_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, \
    current_user, login_required
from itsdangerous import URLSafeTimedSerializer
import os
import sqlalchemy
from hashlib import md5
# end Import's


# Globals
app = Flask(__name__)
app.config.update(dict(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME='chrisddhnt@gmail.com',
    MAIL_PASSWORD=os.environ.get('MAIL_PASS')
))
app.secret_key = 'Any String or Number for encryption here'
title = 'InternREQ-'
app.config.from_object(__name__)
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
app.secret_key = 'Any String or Number for encryption here'
title = 'InternREQ-'
sessionID = []
serial = URLSafeTimedSerializer(app.secret_key)

#   Flask-Login User class
class User(UserMixin):
    # tracks how many times this class has been created 
    # doubles as a unique login id 
    instances = 0
    def __init__(self, user_id, email, password, role, name, last_login):
        self.id = user_id
        self.email = email
        self.pass_hash = generate_password_hash(password)
        self.role = role
        self.name = name
        self.last_login = last_login
        self.uniqueID = User.instances
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
        self.profile = ProfileUser(self.id)

#   End class

#   Profile User Class
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

#   End class


# Database Access

# <!> Set the environment variable before testing locally
# In Windows:   $env:DB_PASS = 'ourpassword'
# In Mac:       export DB_PASS=ourpassword

db_ip = '35.221.39.35'
db_password = os.environ.get('DB_PASS')
db_user = 'root'
db_name = 'internreq'
db_connection_name = 'birmingham4test:us-east4:internreq-1'

# When deployed to App Engine, the `GAE_ENV` environment variable will be
# set to `standard`
if os.environ.get('GAE_ENV') == 'standard':
    # If deployed, use the local socket interface for accessing Cloud SQL
    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    engine_url = 'mysql+pymysql://{}:{}@/{}?unix_socket={}'.format(
        db_user, db_password, db_name, unix_socket)
else:
    # If running locally, use the IP address to connect
    host = db_ip
    engine_url = 'mysql+pymysql://{}:{}@{}/{}'.format(
        db_user, db_password, host, db_name)

db = Database.Database(engine_url)
engine = sqlalchemy.create_engine(engine_url, pool_size=3)



#   Flask-Login login_manager


@login_manager.user_loader
def load_user(id):
    # get user id, email, password, role and name
    sql = 'SELECT * FROM users WHERE user_id="%s"' % (id)
    row = db.query('PULL', sql)[0]
    user_id = row[0]
    email = row[1]
    password = row[2]
    role = row[3]
    name = row[4]
    last_login = row[5]
    user = User(user_id, email, password, role, name, last_login)
    return (user)


#   End manager


@app.route('/')
def landing():
    if(current_user.is_authenticated):
        return redirect(url_for('dashboard'))
    return render_template('landingPage.html', title=title+"-Home")


#   This is the route for login page, when first opening the page it is opened
#   via a GET request and ONLY the last render template executes.
#   If the user clicks submit the POST method executes and server recives entered data and verifies
#   against the database


@app.errorhandler(404)
def page_not_found(a):
    # This route is for handling when an incorrect url is typed
    return render_template('404.html')
  
@app.errorhandler(500)
def server_error(b):
    # This route is for handling when an internal server error occurs
    return render_template('500.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if(current_user.is_authenticated):
        return redirect(url_for('dashboard'))
    form = forms.Login()
    if(form.validate_on_submit()):
        # Retrieve Input from Form
        email = form.email.data
        pwrd = form.password.data

        if(db.credntial_check(email, pwrd)):
            # get user id, email, password, role and name
            sql = 'SELECT * FROM users WHERE email="%s"' % (email)
            row = db.query('PULL', sql)[0]
            user_id = row[0]
            email = row[1]
            password = row[2]
            role = row[3]
            name = row[4]
            last_login = row[5]

            verified = db.query('PULL', "SELECT verified From {} WHERE user_id={}".format(role,user_id))
            # create user object
            if(verified[0][0] == 1): # Block all non-verified users from loggin in
                user = User(user_id, email, password, role, name, last_login)
                login_user(user)
                User.instances += 1
                return redirect(url_for('dashboard'))
            else:
                flash('Account Not Verified. Please Check the email you registered with.', 'danger')
                return(render_template('login.html', title=(title + 'Login'), form=form))
        else:
            flash('Username or Password Error', 'danger')
    return render_template('login.html', title=(title + 'Login'), form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('Logout Successfull', 'success')
    return redirect(url_for('login'))



#   Same as Login: only last line executes at first, upon submit the if statment executes and evaluates
#   against our database. If account not in database: create a new user
#                         Else: foward to login page and request user to login


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = forms.Registration()

    if(form.validate_on_submit()):
        # Retreive inputs
        first = form.first_name.data
        last = form.last_name.data
        user_type = form.user_type.data
        email = form.email.data
        pswrd = form.confirm.data
        pswrd = db.encrypt(pswrd)

        # Pull from Database

        sql = "SELECT * FROM users WHERE email LIKE '%s'" % email

        if(len(db.query('PULL', sql)) == 0):
            sql = "INSERT INTO users (user_id, email, password, role, name) VALUES (%s,%s,%s,%s,%s)"
            args = (0, email, pswrd, user_type, first)
            db.query('PUSH', sql, args)
            # add to sudent/faculty/sponsor table
            sql = "SELECT user_id FROM users WHERE email LIKE '%s'" % email
            user_id = db.query("PULL", sql)
            sql = "INSERT INTO " + user_type + \
                "(user_id, first_name, last_name, email, verified) VALUES(%s,%s,%s,%s, %s)"
            args = (user_id, first, last, email, 0)
            db.query('PUSH', sql, args)

            # Check if it is southern email address
            southern = email.split('@')
            if(southern[1] == 'southernct.edu'):
                token = serial.dumps(email, salt='email-confirm')
                msg = Message(sender='chrisddhnt@gmail.com',subject="Email Verification", recipients=[email])
                link = (url_for('email_confirm', token=token, _external=True))
                msg.body = (
                    'Thanks for signing up. Here is your registration key \n{}').format(link)
                mail.send(msg)
            else:
                msg = Message(sender='chrisddhnt@gmail.com',subject="User Verification", recipients=['chris.conlon1993@gmail.com'])
                link = (url_for('login', _external=True))
                msg.body = ('New Account created for Faculty/Sponsor. Do You want to allow user with email address {} into the system? If yes please login here {} and go to the appropriate page. Else discard this message').format(email,link)
                mail.send(msg)

        else:
            flash("Email address already used! Please Login.", 'danger')
            return redirect(url_for('registration'))

        flash('Account Creation Successful!', 'success')
        return redirect('/login')

    return render_template('registration.html', title=(title+"-Registration"), form=form)


@app.route('/email_confirm/<token>')
def email_confirm(token):
    try:
        email = serial.loads(token, salt='email-confirm', max_age=3600)# token lives for 1 hour
        student = db.query('PULL', "Select user_id FROM users WHERE email='{}'".format(email))
        db.query('PUSH', "UPDATE student SET verified=TRUE WHERE user_id={}".format(student[0][0]))
    except Exception:
        flash('Your verification link has expired please re-register')
        return redirect('/scoobysnacks')
    flash('Account Verified!')
    return(redirect(url_for('login')))

    
@app.route('/user_confirm', methods=['GET', 'POST'])
def user_confirm():
    if(not(current_user.is_authenticated) or current_user.role != 'faculty'):
        return render_template('unauthorized.html')
    else:
        form = forms.AddUser()
        if(form.validate_on_submit()):
            email = form.email.data
            sql = "SELECT * FROM users WHERE email='{}'".format(email)
            user = db.query('PULL', sql)
            if(len(user) != 0):
                user = user[0]
                sql = "UPDATE {} SET verified=True WHERE user_id={}".format(user[3], user[0]) # update <role_table> with a true value in verified 
                db.query('PUSH',sql)
                flash('User has been verified.', 'success')
            else:
                flash('No user with the email address is registered', 'danger')
            return(redirect(url_for('user_confirm', form=form)))
        return(render_template('AddUser.html', form=form))

#   Skeleton code for user profile


@app.route('/profile/<user_id>', methods=['GET', 'POST'])
def profile(user_id):
    if (current_user.is_authenticated):  # if user is authenticated
        if db.query("PULL", "SELECT role FROM users WHERE user_id = %s" % (user_id)):  # if user profile exists

            # create profile_user object from class
            profile_user = ProfileUser(user_id)

            # Enable Edit Profile (if logged in user's profile by user_id)
            if(int(user_id) == current_user.id):
                return render_template('profile.html', profile_user=current_user.profile, Edit=True)
            return render_template('profile.html', profile_user=profile_user, Edit=False)
        else:
            flash('This is not the user you are looking for.', 'danger')
            return render_template('404.html')
    else:
        return redirect('/login')

'''
This is the code for editing profile. The user is presented the data currently
linked to their account and is able to edit these values and have the changes
reflected in their profile page
'''
@app.route('/profile/<user_id>/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile(user_id):
    x = int(user_id)
    y = int(current_user.id)
    if (x != y):
        flash('You cannot edit profiles other than your own')
        return redirect(url_for('dashboard'))
    else:
        form = forms.EditProfile()
        if request.method == 'GET':
            if(current_user.role == 'faculty'):
                sql =  "SELECT first_name FROM faculty WHERE user_id = %s" % (user_id)
                first_name = db.query('PULL',sql)[0][0]
                form.first_name.data = first_name
                sql =  "SELECT last_name FROM faculty WHERE user_id = %s" % (user_id)
                last_name = db.query('PULL',sql)[0][0]
                form.last_name.data = last_name
                sql =  "SELECT title FROM faculty WHERE user_id = %s" % (user_id)
                user_title = db.query('PULL',sql)[0][0]
                form.user_title.data = user_title
                sql =  "SELECT department FROM faculty WHERE user_id = %s" % (user_id)
                department = db.query('PULL',sql)[0][0]
                form.department.data = department
                sql =  "SELECT location FROM faculty WHERE user_id = %s" % (user_id)
                location = db.query('PULL',sql)[0][0]
                form.location.data = location
                sql =  "SELECT about FROM faculty WHERE user_id = %s" % (user_id)
                about = db.query('PULL',sql)[0][0]
                form.about.data = about
                return render_template('edit_profile.html', title='Edit Profile',
                           form=form, first_name=first_name, last_name=last_name, user_title=title, department = department,
                           location = location, about = about)
        if (request.method == 'POST'):
            if(current_user.role == 'faculty'):
                sql = "UPDATE faculty SET first_name = '%s' WHERE user_id = %s" % (form.first_name.data, user_id)
                db.query('UPDATE', sql)
                sql = "UPDATE faculty SET last_name = '%s' WHERE user_id = %s" % (form.last_name.data, user_id)
                db.query('UPDATE', sql)
                sql = "UPDATE faculty SET title = '%s' WHERE user_id = %s" % (form.user_title.data, user_id)
                db.query('UPDATE', sql)
                sql = "UPDATE faculty SET department = '%s' WHERE user_id = %s" % (form.department.data, user_id)
                db.query('UPDATE', sql)
                sql = "UPDATE faculty SET location = '%s' WHERE user_id = %s" % (form.location.data, user_id)
                db.query('UPDATE', sql)
                sql = "UPDATE faculty SET about = '%s' WHERE user_id = %s" % (form.about.data, user_id)
                db.query('UPDATE', sql)
                return redirect(url_for('profile', user_id=current_user.id))
    return render_template('edit_profile.html', title='Edit Profile', form=form)
    
'''
Skeleton code for dashboard
'''
@app.route('/dashboard')
@login_required
def dashboard():
    if(current_user.is_authenticated):
        name = current_user.name
        postings = db.query('PULL', 'SELECT * FROM internship')
        applications = []
        user_id = str(current_user.id)
        if(current_user.role == 'student'):
            posting = db.query('PULL', 'SELECT * FROM applications WHERE user_id=' + user_id)
            for x in range(len(posting)):
                applications.append(db.query(
                    'PULL', 'SELECT * FROM internship WHERE internship_id={}'.format(posting[x][1]))[0])
        elif(current_user.role == 'sponsor'):
            posting = db.query('PULL', 'SELECT * FROM internship WHERE user_id=' + user_id)
            for x in range(len(posting)):
                applications.append(db.query(
                    'PULL', 'SELECT * FROM internship WHERE user_id={}'.format(posting[x][1]))[0])

        return render_template('dashboard.html', title=(title+'Dashboard'),applied=applications, name=name, Daily="Welcome to the Program", postings=postings)
    return redirect('/login')


@app.route('/posting/<id>', methods=['GET', 'POST'])
def posting(id):

    if request.method == 'POST':
        sql = 'INSERT INTO applications(user_id, internship_id) VALUES(%s,%s)'
        args = (current_user.id, id)
        db.query('PUSH', sql, args)
        flash('Application Submited', 'success')
    # when loading posting we do not need the ID or user ID so start at title and go from there ([0][3:])
    posting = db.query(
        'PULL', "SELECT * FROM internship WHERE internship_id="+id)[0][3:]
    return render_template('posting.html', datePosted=1, postingInfo=posting)


@app.route('/create/posting', methods=['GET', 'POST'])
@login_required
def createPosting():
    if(current_user.role == 'sponsor' or current_user.role == 'faculty'):
        form = forms.Posting()
        if(form.validate_on_submit()):
            title = form.title.data
            location = form.location.data
            overview = form.overview.data
            repsons = form.responsibilities.data
            reqs = form.reqs.data
            comp = form.comp.data
            jType = form.fullPart.data
            hours = form.hours.data
            sql = "INSERT INTO internship(internship_id, user_id, title," \
                " location, overview, responsibilities, requirements, compensation, type, availability)VALUES"\
                "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            args = (0, current_user.id, title, location,
                    overview, repsons, reqs, comp, jType, hours)
            db.query('PUSH', sql, args)
            return redirect('/profile/'+str(current_user.id))
        return(render_template('posting.html', form=form))
    return(render_template('unauthorized.html'))


def send_email(subject, sender, recipients, body):
    msg = Message(subject, sender=sender, recipients=[recipients])
    msg.html = body
    mail.send(msg)


@app.route('/testemail')
def testemail():
    send_email("Thank You", 'chrisddhnt@gmail.com',
               current_user.email, "<h1>Test Email recived</h1>")
    flash('email sent', 'success')
    return(redirect(url_for('dashboard')))

@app.route('/admin_view')
@login_required
def admin_view():
    userTable = db.query('PULL', "Select * from users")
    studentTable = db.query('PULL', "Select * from student")
    sponsorTable = db.query('PULL', "Select * from sponsor")
    facultyTable = db.query('PULL', "Select * from faculty")
    return render_template('adminView.html', users=userTable,students=studentTable,sponsors=sponsorTable, facultyM=facultyTable)

if (__name__ == "__main__"):
    if os.environ.get('GAE_ENV') != 'standard':
        app.run(host='0.0.0.0', port='8080', debug=True)
