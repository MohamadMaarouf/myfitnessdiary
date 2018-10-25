''' Flask server to handle routing for InternREQ.com. '''

# Import's
import getpass
import pymysql
from modules import forms
from flask import Flask, flash, redirect, render_template, request, session, url_for
# end Import's
'''
Authors:
    Tom Birmingham
    Christopher Conlon
    Daniel G.
    Davis Jaekle
    Mohamad M.
'''

# Gloabls
app = Flask(__name__)
app.secret_key = 'Any String or Number for encryption here'
title = 'InternREQ-'


# Database Access
IP = '35.221.39.35'
pas = getpass.getpass('Enter Password for InternREQ DB: ')


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

        # Database Connect
        db = pymysql.connect(host=IP, user='root',
                             password=pas, db='internreq')
        c = db.cursor()
        c.execute('SELECT * FROM  users WHERE  email="'+email+'"')
        l = c.fetchall()  # With this tuple we can parse for information to assign each user

        db.close()

        if(len(l) != 0 and l[0][1] == email and l[0][2] == pwrd):
            session['Username'] = email
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
        user_type = form.user_type.data
        email = form.email.data
        pswrd = form.confirm.data

        # Pull from Database
        db = pymysql.connect(host=IP, user='root',
                             password=pas, db='internreq')
        c = db.cursor()
        c.execute('Select * from users where email="' +
                  email+'"')
        l = c.fetchall()  # With this tuple we can parse for information to assign each user
        # ((1, 'chris.conlon1993@gmail.com', 'password', 'faculty admin'),)

        if(len(l) == 0):
            sql = "INSERT INTO users(user_id, email, password, role) VALUES" \
                "(%s,%s,%s,%s)"
            c.execute(sql, (int(0), email, pswrd, user_type))
            c.execute("Select * from users")
            print(c.fetchall())
            db.commit()
            db.close()
        else:
            flash("Email address already used! Please Login.", 'danger')
            db.close()
            return redirect('/registration')
        flash('Account Creation Successful!', 'success')
        return redirect('/login')

    return render_template('registration.html', title=(title+"-Registration"), form=form)


'''
Skeleton code for user profile
'''


@app.route('/profile/<user>')
def profile(user):
    if(session['Username'] == user):
        return (render_template('profile.html', Username=user, title=(title+"-Profile")))
    session.pop('Username', None)

    return redirect('/login')


'''
Skeleton code for dashboard
'''


@app.route('/dashboard/<name>')
def dashboard(name):
    if(session['Username'] == name):
        return render_template('dashboard.html', title=(title+'Dashboard'), Username=name)
    session.pop('Username', None)
    return redirect('/login')


if (__name__ == "__main__"):
    app.run(host='0.0.0.0', port=8080, debug=True)
