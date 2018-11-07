''' Flask server to handle routing for InternREQ.com. '''

# Import's
import getpass
from modules import forms, Database
from flask import Flask, flash, redirect, render_template, request, session, url_for
from hashlib import md5
# end Import's

# Gloabls
app = Flask(__name__)
app.secret_key = 'Any String or Number for encryption here'
title = 'InternREQ-'


# Database Access
# <!> for connection issues ask TOM for password and to whitelist your IP </!>
IP = '35.196.126.63' # Chris's IP
IP = '35.221.39.35' # Gear Grinders Official DB

pas = getpass.getpass('Enter Password for InternREQ DB: ')
db = Database.Database(IP, 'root', pas, 'internreq')


@app.route('/')
def landing():
    return render_template('landingPage.html', title=title+"-Home")


'''
This is the route for login page, when first opening the page it is opened
via a GET request and ONLY the last render template executes.
If the user clicks submit the POST method executes and server recives entered data and verifies
against the database
'''


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.Login()
    if(form.validate_on_submit()):
        # Retrieve Input from Form
        email = form.email.data
        pwrd = form.password.data

        if(db.credntial_check(email, pwrd)):
            # set a session cookie with values: Username, Role, ID, Name
            session['Username'] = email
            session['Email'] = email
            session['Role'] = db.query(
                'PULL', "SELECT role FROM users WHERE email LIKE '%s'" % email)[0][0]
            session['ID'] = db.query(
                'PULL', "SELECT user_id FROM users WHERE email LIKE '%s'" % email)[0][0]  # [0][0] gives us the integer rather then tuple
            sql = "SELECT first_name, last_name FROM %s WHERE user_id = %s" % (session['Role'], session['ID'])
            result = db.query("PULL", sql)
            session['Name'] = result[0][0]
            full_name = result[0][0] + ' ' + result[0][1]
            session['Full Name'] = full_name
            session['Authenticated'] = True
            session['User_id'] = db.query(
                'PULL', "SELECT user_id FROM users WHERE email LIKE '%s'" % email)[0][0]
            return redirect('/dashboard')
        else:
            flash('Username or Password Error', 'danger')

    return render_template('login.html', title=(title + 'Login'), form=form)


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
    if (session.get('Authenticated')):
        # if profile has been created for this user
        sql = "SELECT role FROM users WHERE user_id = %s" % (user_id)
        if (db.query("PULL", sql)):
            # get role
            sql = "SELECT role FROM users WHERE user_id = %s" % (user_id)
            role = db.query("PULL", sql)[0][0]
            # get name, title, major, location
            sql = "SELECT first_name, last_name FROM %s WHERE user_id = %s" % (role, user_id)
            result = db.query("PULL", sql)
            name = result[0][0] + ' ' + result[0][1] # flatten tuple
            sql = "SELECT title FROM %s WHERE user_id = %s" % (role, user_id)
            title = db.query("PULL", sql)[0][0]
            sql = "SELECT department FROM %s WHERE user_id = %s" % (role, user_id)
            department = db.query("PULL", sql)[0][0]
            sql = "SELECT location FROM %s WHERE user_id = %s" % (role, user_id)
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
            if( int(user_id) == int(session.get('User_id'))):
                edit = True
            else:
                edit = False
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
def dashboard():
    if(session.get('Authenticated')):
        name = session.get('Name')
        return render_template('dashboard.html', title=(title+'Dashboard'), name=name)
    else:
        return redirect('/login')


@app.route('/posting/<id>')
def posting(id):
    # when loading posting we do not need the ID or user ID so start at title and go from there ([0][3:])
    posting = db.query(
        'PULL', "SELECT * FROM internship WHERE internship_id="+id)[0][3:]
    return render_template('posting.html', datePosted=1, postingInfo=posting)


@app.route('/create/posting', methods=['GET','POST'])
def createPosting():
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
        "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % (0, session['ID'], title, location, overview,repsons,reqs,comp,jType, hours)
        db.query('PUSH',sql)
        return redirect('/profile/'+session['Username'])
    return (render_template('posting.html', datePosted=1, form=form))


if (__name__ == "__main__"):
    app.run(host='0.0.0.0', port=8080, debug=True)
