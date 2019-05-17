''' Flask server to handle routing for MyFitnessDiary '''

# Import's
from modules import forms, Database
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_mail import Mail
from flask_mail import Message
# Flask-Login attempt import's
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask_login import LoginManager, UserMixin, login_user, logout_user, \
    current_user, login_required
from itsdangerous import URLSafeTimedSerializer
import os
import sqlalchemy
from hashlib import md5
from google.cloud import storage
from google.cloud.storage import Blob
# end Import's


# Globals
application_title = 'MyFitnessDiary'
application = Flask(__name__)
application.secret_key = 'Any String or Number for encryption here'

# Mail Configuration    <!> Set environment variable before testing locally
#       Windows (powershell):     $env:MAIL_PASS = 'ourpassword'
#       Winders (CMD):            set MAIL_PASS=ourpassword
#       Mac (Terminal):           export MAIL_PASS=ourpassword
application.config.update(dict(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME='',
    MAIL_PASSWORD=''
))
application.config.from_object(__name__)
mail = Mail(application)

login_manager = LoginManager(application)
login_manager.login_view = 'login'

sessionID = []
serial = URLSafeTimedSerializer(application.secret_key)
ALLOWED_EXTENSIONS = set(['pdf'])

# Database Access   <!> Set environment variable before testing locally
#       Windows:   $env:DB_PASS = 'ourpassword'
#       Windows:   set DB_PASS=ourpassword
#       Mac:       export DB_PASS=ourpassword
db_ip = '35.196.253.182' #MyFitnessDiary database
#db_ip = 'localhost'
db_password = ''
db_user = 'root'
db_name = 'MyFitnessDiary'
db_connection_name = 'myfitnessdiary:us-east1:myfitnessdiary'

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
# End Globals


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
        #TODO: create profile objet for all users in python
        # self.profile = ProfileUser(self.id)
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
        self.location = row[4]
        self.about = row[5]
        self.url = row[6]
        self.goalWeight = row[7]
        self.mainExercise = row[8]
        self.workoutOne = row[9]
        self.workoutTwo = row[10]
        self.workoutThree = row[11]
        self.verified = row[12]
        self.private = row[13]
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

#   End class

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

# Error Pages Routes
"""@application.errorhandler(404)
def page_not_found(a):
    # This route is for handling when an incorrect url is typed
    return render_template('404.html', title=application_title)
  
@application.errorhandler(500)
def server_error(b):
    # This route is for handling when an internal server error occurs
    return render_template('500.html', title=application_title)

@application.errorhandler(Exception)
def all_other_errors(c):
    # This route is for catching all non 404 or 500 errors
    return render_template('Exception.html', title=application_title)"""

# Landing Page Route 
@application.route('/')
def landing():
    if(current_user.is_authenticated):
        return redirect(url_for('dashboard'))
    return render_template('landingPage.html', title=application_title)


#   Login Page Route
#   This is the route for login page, when first opening the page it is opened
#   via a GET request and ONLY the last render template executes.
#   If the user clicks submit the POST method executes and server recives entered data and verifies
#   against the database
@application.route('/login', methods=['GET', 'POST'])
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
                return(render_template('login.html', title=application_title, form=form))
        else:
            flash('Username or Password Error', 'danger')
    return render_template('login.html', title='Login | '+application_title, form=form)


#   Logout Route
@application.route('/logout')
def logout():
    logout_user()
    flash('Logout Successfull', 'success')
    return redirect(url_for('login'))

#   Registration Page Route
#   Same as Login: only last line executes at first, upon submit the if statment executes and evaluates
#   against our database. If account not in database: create a new user
#                         Else: foward to login page and request user to login
@application.route('/registration', methods=['GET', 'POST'])
def registration():
    form = forms.Registration()

    if(form.validate_on_submit()):
        # Retreive inputs
        first = form.first_name.data
        last = form.last_name.data
        email = form.email.data
        pswrd = form.confirm.data
        pswrd = db.encrypt(pswrd)
        url = form.email.data

        # Pull from Database
        sql = "SELECT * FROM users WHERE email LIKE '%s'" % email

        if(len(db.query('PULL', sql)) == 0):
            sql = "INSERT INTO users (user_id, email, password, role, name) VALUES (%s,%s,%s,%s,%s)"
            args = (0, email, pswrd, 'member', first)
            db.query('PUSH', sql, args)
            # add to member table
            sql = "SELECT user_id FROM users WHERE email LIKE '%s'" % email
            user_id = db.query("PULL", sql)[0][0]
            sql = "INSERT INTO "+ 'member' +" (user_id, first_name, last_name, url, verified) VALUES(%s,%s,%s,%s,%s)"
            args = (user_id, first, last, url, 1)
            db.query('PUSH', sql, args)

        else:
            flash("Email address already used! Please Login.", 'danger')
            return redirect(url_for('registration'))

        flash('Account Creation Successful!', 'success')
        return redirect('/login')

    return render_template('registration.html', title='Registration | '+application_title, form=form)


#   Profile Page Route
@application.route('/profile/<user_id>', methods=['GET', 'POST'])
def profile(user_id):
    if (current_user.is_authenticated):  # if user is authenticated
        # if user profile exists
        if db.query("PULL", "SELECT role FROM users WHERE user_id = %s" % (user_id)):
            role = db.query("PULL", "SELECT role FROM users WHERE user_id = {}".format(user_id))[0][0]
            private = db.query("PULL", "SELECT private FROM {} WHERE user_id = {}".format(role,user_id))
            if(private[0][0]):
                privacy = 'Private'
            else:
                privacy = 'Public'

            if(private[0][0] and current_user.id != int(user_id)):
                flash("User's profile is private", 'danger')
                return redirect('/scoobysnacks')

            # create profile_user object from class
            profile_user = ProfileUser(user_id)

            # Enable Edit Profile (if logged in user's profile by user_id)
            if(int(user_id) == current_user.id):
                edit = True
            else:
                edit = False
            page_title = profile_user.full_name+' | '
            return render_template('profile.html', title=page_title+application_title, profile_user=profile_user, Edit=edit, Privacy = privacy)
        else:
            # profile does not exist
            return render_template('404.html', title=application_title)
    else:
        return redirect('/login')

#   Edit Profile Route
#   This is the code for editing profile. The user is presented the data currently
#   linked to their account and is able to edit these values and have the changes
#   reflected in their profile page

@application.route('/profile/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user_id = current_user.id
    form = forms.EditProfileM()
    if (request.method == 'GET'):
        sql = "SELECT first_name, last_name, title, location, about, goalWeight, mainExercise, workoutOne, workoutTwo, workoutThree, private, url FROM member WHERE user_id = %s" % (user_id)
        form.first_name.data, form.last_name.data, form.user_title.data, form.location.data, form.about.data, form.goalWeight.data, form.mainExercise.data, form.workoutOne.data, form.workoutTwo.data, form.workoutThree.data, form.private.data, form.url.data = db.query('PULL', sql)[0]
        return render_template('edit_profileM.html', title='Edit Profile', form=form)
    else:
        new_private = str(form.private.data)
        if(new_private is 'True'):
            flag = True
        else:
            flag = False
        sql = "UPDATE member SET first_name = '%s', last_name = '%s', title = '%s', location = '%s', about = '%s', mainExercise = '%s', goalWeight = '%s', workoutOne = '%s', workoutTwo = '%s', workoutThree = '%s', private = %s, url = '%s'WHERE user_id = %s" % (form.first_name.data, form.last_name.data, form.user_title.data, form.location.data, form.about.data, form.mainExercise.data, form.goalWeight.data, form.workoutOne.data, form.workoutTwo.data, form.workoutThree.data, flag, form.url.data, user_id)
        db.engine.execute(sql)
        return redirect(url_for('profile', user_id=current_user.id))       

    

#   Dashboard Page Route
@application.route('/dashboard')
@login_required
def dashboard():
    if(current_user.is_authenticated):
        name = current_user.name
        user_id = str(current_user.id)
        postings = db.query('PULL', 'SELECT * FROM diaryPosting WHERE member_id=' + user_id)
        applications = []
        appicants=""
        user_id = str(current_user.id)
        if(current_user.role == 'member'):
            posting = db.query('PULL', 'SELECT * FROM diaryPosting WHERE member_id=' + user_id)



        return render_template('dashboard.html', title=('Dashboard | '+application_title), name=name, Daily="Welcome to the Program", postings=postings)
    return redirect('/login')


#   Diary Posting Page Route
@application.route('/posting/<id>', methods=['GET', 'POST'])
def posting(id):
    # when loading posting we do not need the ID or user ID so start at title and go from there ([0][3:])
    posting = db.query(
        'PULL', "SELECT * FROM diaryPosting WHERE diary_id="+id)[0][3:]
    post_title = posting[1]
    post_type = posting[1]
    page_title = post_title+' - '+post_type+' | '
    return render_template('posting.html', title=page_title+application_title, datePosted=1, postingInfo=posting)


#   Create Diary Posting Route
@application.route('/create/posting', methods=['GET', 'POST'])
@login_required
def createPosting():
    if(current_user.role == 'member'):
        form = forms.Posting()
        if(form.validate_on_submit()):
            dateOfPost = form.dateOfPost.data
            exercise = form.exercise.data
            overview = form.overview.data
            current = form.current.data
            goal = form.goal.data
            sql = "INSERT INTO diaryPosting(diary_id, member_id, dateOfPost," \
                " exercise, overview, current, goal)VALUES"\
                "(%s,%s,%s,%s,%s,%s,%s)"
            args = (0, current_user.id, dateOfPost, exercise,
                    overview, current, goal)
            db.query('PUSH', sql, args)
            return redirect('/profile/'+str(current_user.id))
        return(render_template('posting.html', title='Create Posting | '+application_title, form=form))
    return(render_template('unauthorized.html'))

@application.route('/graph', methods=['GET', 'POST'])
@login_required
def graph():
    form = forms.graphOptions()
    user_id = str(current_user.id)
    """postings = db.query('PULL', 'SELECT * FROM diaryPosting WHERE member_id=' + user_id)"""
    if(form.validate_on_submit()):
        exerciseChosen = str(form.exercise.data)
        print(exerciseChosen)

        timeScale = form.timeScale.data
        postings = db.query('PULL', 'SELECT dateofPost FROM diaryPosting')
        print(postings)
        #months = db.query('PULL', 'SELECT distinct month(dateOfPost), year(dateOfPost) FROM diaryPosting WHERE member_id=' + user_id)
        months = db.query('PULL', 'SELECT distinct month(dateOfPost), year(dateOfPost) FROM diaryPosting WHERE member_id='+ user_id + ' AND exercise="{}"'.format(exerciseChosen) + ' ORDER BY year(dateOfPost), month(dateOfPost) asc')
        print(months)
        years = db.query("PULL", 'SELECT distinct year(dateOfPost) FROM diaryPosting WHERE member_id=' + user_id + ' AND exercise="{}"'.format(exerciseChosen)+ ' ORDER BY year(dateOfPost) asc')
        days = db.query("PULL", 'SELECT month(dateOfPost), day(dateOfPost), year(dateOfPost) FROM diaryPosting WHERE member_id=' + user_id + ' AND exercise="{}"'.format(exerciseChosen)+ ' ORDER BY year(dateOfPost), month(dateOfPost), day(dateOfPost) asc')
        weight = db.query('PULL','SELECT current FROM diaryPosting WHERE member_id=' + user_id + ' AND exercise="{}"'.format(exerciseChosen))
        print(exerciseChosen)

        user_id = str(current_user.id)
        if timeScale == 'Day':
            labels = days
            value = db.query('PULL', 'SELECT current from diaryPosting WHERE member_id=' + user_id + ' AND exercise="{}"'.format(exerciseChosen) +' ORDER BY dateOfPost asc')
            x = 0
            values=[]
            while x<len(labels):
                tuplenum = value[x]
                tupleint = tuplenum[0]
                values.append(tupleint)
                x=x+1
        elif timeScale == 'Month':
            labels = months
            print(exerciseChosen)
            value = db.query('PULL', 'SELECT current from diaryPosting WHERE member_id=' + user_id + ' AND exercise="{}"'.format(exerciseChosen) +' ORDER BY month(dateOfPost), year(dateOfPost) asc')

            #value = db.query('PULL', 'SELECT current from diaryPosting WHERE exercise=' + exerciseChosen + ' ORDER BY month(dateOfPost), year(dateOfPost)')
            x = 0
            values=[]
            while x<len(labels):
                tuplenum = value[x]
                tupleint = tuplenum[0]
                values.append(tupleint)
                x=x+1
            
        else:
            labels = years
            value = db.query('PULL', 'SELECT current from diaryPosting  WHERE member_id=' + user_id + ' AND exercise="{}"'.format(exerciseChosen) +' ORDER BY year(dateOfPost) asc')
            x = 0
            values=[]
            while x<len(labels):
                tuplenum = value[x]
                tupleint = tuplenum[0]
                values.append(tupleint)
                x=x+1
        print(values)
        line_labels=labels
        line_values=values 
        return render_template('graph.html', title=exerciseChosen+' Max Growth Over Time', max=315, labels=line_labels, values=line_values)
    return render_template('graphOptions.html', title='Edit Profile', form=form)

#   Send Mail Route
def send_email(subject, sender, recipients, body):
    msg = Message(subject, sender=sender, recipients=[recipients])
    msg.html = body
    mail.send(msg)


#   Admin Tables View Route
@application.route('/members_panel')
@login_required
def members_panel():
    userTable = db.query('PULL', "Select * from users")
    memberTable = db.query('PULL', "Select * from member")
    return render_template('membersPanel.html', title='Member Panel | '+application_title, users=userTable, members=memberTable)


#   Users Search Route
@application.route('/results/<user_search>')
@login_required
def general_search(user_search):
    user_id = str(current_user.id)
    user_results = db.query('PULL', "SELECT * from users WHERE name LIKE '%%{}%%'".format(user_search))
    member_results = db.query('PULL', "Select * from member WHERE first_name LIKE '%%{}%%'".format(user_search) + " OR last_name LIKE '%%{}%%'".format(user_search))
    diaryPosting_results = db.query('PULL', "Select * from diaryPosting WHERE member_id=" +user_id+ " AND exercise LIKE '%%{}%%'".format(user_search) + " OR member_id=" +user_id + " AND dateOfPost LIKE '%%{}%%'".format(user_search))
    return render_template('searchResults.html', users=user_results, members=member_results, diaries=diaryPosting_results, title='Results For "'+user_search+'"')


#   Search Helper Route
@application.route('/search_handler',methods=['POST'])
def search_handler():
    search = request.form['searchingFor']
    if('%20' in search):
        search.replace('%20', " ")
    return (redirect( url_for("general_search", user_search=search) ))


if (__name__ == "__main__"):
    if os.environ.get('GAE_ENV') != 'standard': # if not deployed to the application engine
        application.run(host='0.0.0.0', port='8080', debug=True)
