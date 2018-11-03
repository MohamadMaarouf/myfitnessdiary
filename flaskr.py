''' Flask server to handle routing for InternREQ.com. '''

# Import's
import getpass
from modules import forms, Database
from flask import Flask, flash, redirect, render_template, request, session, url_for
# end Import's

# Gloabls
app = Flask(__name__)
app.secret_key = 'Any String or Number for encryption here'
title = 'InternREQ-'


# Database Access
IP = '35.196.126.63'
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
            # set a session cookie with values role and ID that refrences our tables
            session['Username'] = email
            session['Role'] = db.query(
                'PULL', "SELECT role FROM users WHERE email LIKE '%s'" % email)[0][0]
            session['ID'] = db.query(
                'PULL', "SELECT user_id FROM users WHERE email LIKE '%s'" % email)[0][0]  # [0][0] gives us the integer rather then tuple
            route = '/dashboard/' + email
            return redirect(route)
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


@app.route('/profile/<user>', methods=['GET', 'POST'])
def profile(user):
    if('Username' in session and session['Username'] == user):
        first = db.query("PULL", "Select first_name from " +
                         (session['Role'])+" where user_id="+str(session['ID']))[0][0]
        last = db.query("PULL", "Select last_name from " +
                        (session['Role'])+" where user_id="+str(session['ID']))[0][0]
        name = first + " " + last
        return render_template('profile.html', Username=name, Edit=True)
    return render_template('profile.html', Username=user)


'''
Skeleton code for dashboard
'''


@app.route('/dashboard/<name>')
def dashboard(name):
    if(session['Username'] == name):
        return render_template('dashboard.html', title=(title+'Dashboard'), Username=name)
    session.pop('Username', None)
    return redirect('/login')


@app.route('/posting')
def posting():
    return render_template('posting.html', datePosted=1)


@app.route('/create/posting')
def createPosting():
    form = forms.Posting()
    if(form.validate_on_submit()):
        return redirect('/profile/'+session['Username'])
    return (render_template('posting.html', datePosted=1, form=form))


if (__name__ == "__main__"):
    app.run(host='0.0.0.0', port=8080, debug=True)
