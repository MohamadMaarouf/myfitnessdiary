''' Flask server to handle routing for InternREQ.com. '''

# Import's
import getpass
from random import randint
from modules import forms, Database
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_mail import Mail
from flask_mail import Message
from hashlib import md5
# Flask-Login attempt import's
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, \
    current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
# end Import's


# Gloabls
app = Flask(__name__)
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'chrisddhnt@gmail.com',
    MAIL_PASSWORD = 'internreq',
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

'''Flask-Login User class'''


class User(UserMixin):
    def __init__(self, user_id, email, password, role):
        self.id = user_id
        self.email = email
        self.pass_hash = generate_password_hash(password)
        self.role = role
        # Create a uniqueID for each login
        uniqueID = randint(0, 100000000000000000000000000000)
        # If the ID is already in our list recreate another one
        while(uniqueID in sessionID):
            uniqueID = randint(0, 100000000000000000000000000000)
        # Once unique id is found append it to the in use ID's and assign it to the user
        sessionID.append(uniqueID)
        self.uniqueID = uniqueID
        ''' Once we reset the server all IDs are droped as well and frees up each number to be re-used'''


'''End class'''


# Database Access
# <!> for connection issues ask TOM for password and to whitelist your IP </!>
IP = '35.221.39.35' # Gear Grinders Official DB

pas = getpass.getpass('Enter Password for InternREQ DB: ')
db = Database.Database(IP, 'root', pas, 'internreq')

''' Flask-Login login_manager'''
@login_manager.user_loader
def load_user(id):
    sql = 'SELECT * from users WHERE user_id="%s"' % (id)
    row = db.query('PULL', sql)[0]
    user = User(row[0], row[1], row[2], row[3])
    return (user)
''' End manager '''

@app.route('/')
def landing():
    return render_template('landingPage.html', title=title+"-Home")


'''


This is the route for login page, when first opening the page it is opened
via a GET request and ONLY the last render template executes.
If the user clicks submit the POST method executes and server recives entered data and verifies
against the database
'''

@app.errorhandler(404):
def page_not_found(a):
    # This route is for handling when an incorrect url is typed
    return render_template('404.html')

@app.errorhandler(500):
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
            sql = 'Select * from users WHERE email="%s"' % (email)
            row = db.query('PULL', sql)[0]
            user = User(row[0], row[1], row[2], row[3])
            login_user(user)
            print(current_user.uniqueID)
            return redirect(url_for('dashboard'))
        else:
            flash('Username or Password Error', 'danger')

    return render_template('login.html', title=(title + 'Login'), form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('Logout Successfull', 'success')
    return redirect(url_for('login'))


'''
Same as Login: only last line executes at first, upon submit the if statment executes and evaluates
against our database. If account not in database: create a new user
                      Else: foward to login page and request user to login
'''


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = forms.Registration()

    if(form.validate_on_submit()):
        # Retreive inputs
        first = form.first_name.data
        last = form.last_name.data
        user_type = form.user_type.data
        vKey = form.v_key.data
        email = form.email.data
        pswrd = form.confirm.data

        # Pull from Database

        sql = "SELECT * FROM users WHERE email LIKE '%s'" % email

        if(len(db.query('PULL', sql)) == 0):
            db.register(first, last, user_type, vKey, email, pswrd)
            # add to sudent/faculty/sponsor table
            sql = "SELECT user_id FROM users WHERE email LIKE '%s'" % email
            user_id = db.query("PULL", sql)
            sql = "INSERT INTO %s (user_id, first_name, last_name) VALUES(%s,%s,%s)" % user_type, user_id, first, last
            db.query('PUSH', sql)
            send_email("Thank You", 'admin@internreq.com', email, "Thank you for registering with InternREQ")


        else:
            flash("Email address already used! Please Login.", 'danger')
            return redirect('/registration')

        flash('Account Creation Successful!', 'success')
        return redirect('/login')

    return render_template('registration.html', title=(title+"-Registration"), form=form)


'''
Skeleton code for user profile
'''


@app.route('/profile/<user_id>', methods=['GET', 'POST'])
def profile(user_id):
    if (current_user.is_authenticated):
        # if profile has been created for this user
        sql = "SELECT role FROM users WHERE user_id = %s" % (user_id)
        if (db.query("PULL", sql)):
            # get role
            sql = "SELECT role FROM users WHERE user_id = %s" % (user_id)
            role = db.query("PULL", sql)[0][0]
            # get name, title, major, location
            sql = "SELECT first_name, last_name FROM %s WHERE user_id = %s" % (
                role, user_id)
            result = db.query("PULL", sql)
            name = result[0][0] + ' ' + result[0][0] # flatten tuple
            sql = "SELECT title FROM %s WHERE user_id = %s" % (role, user_id)
            title = db.query("PULL", sql)[0][0]
            sql = "SELECT department FROM %s WHERE user_id = %s" % (
                role, user_id)
            department = db.query("PULL", sql)[0][0]
            sql = "SELECT location FROM %s WHERE user_id = %s" % (
                role, user_id)
            location = db.query("PULL", sql)[0][0]
            # get about
            sql = "SELECT about FROM %s WHERE user_id = %s" % (role, user_id)
            about = db.query("PULL", sql)[0][0]
            # get user avatar by email (powered by Gravatar)
            sql = "SELECT email FROM users WHERE user_id = %s" % (user_id)
            email = db.query("PULL", sql)[0][0]
            size = 128
            digest = md5(email.lower().encode('utf-8')).hexdigest()
            avatar = 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

            # Enable Edit Profile (if logged in user's profile by user_id)
            edit = False
            if( int(user_id) == current_user.id):
                edit = True
            return render_template('profile.html', avatar=avatar, name=name, title=title, department=department, location=location, about=about, Edit=edit)
        else:
            # TODO: Error page for no profile
            name = 'User Profile not created yet :('
            return render_template('profile.html', name=name)
    else:
        return redirect('/login')


'''
Skeleton code for dashboard
'''
@app.route('/dashboard')
@login_required
def dashboard():
    if(current_user.is_authenticated):
        name = current_user.email
        return render_template('dashboard.html', title=(title+'Dashboard'), name=name)
    return redirect('/login')


def send_email(subject, sender, recipients, body):
    msg = Message(subject, sender=sender, recipients=[recipients])
    msg.body = body
    mail.send(msg)
    
@app.route('/posting/<id>')
def posting(id):
    # when loading posting we do not need the ID or user ID so start at title and go from there ([0][3:])
    posting = db.query(
        'PULL', "SELECT * FROM internship WHERE internship_id="+id)[0][3:]
    return render_template('posting.html', datePosted=1, postingInfo=posting)


@app.route('/create/posting', methods=['GET','POST'])
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
            "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % (0,current_user.id, title, location, overview,repsons,reqs,comp,jType, hours)
            db.query('PUSH',sql)
            return redirect('/profile/'+current_user.id)
    return(render_template('unauthorized.html'))


if (__name__ == "__main__"):
    app.run(host='0.0.0.0', port=8080, debug=True)



