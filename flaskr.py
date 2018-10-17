''' Flask server to handle routing for InternREQ.com. '''

'''
Authors:
    Tom Birmingham
    Christopher Conlon
    Daniel G.
    Davis Jaekle
    Mohamad M.
'''
# Import's
from flask import Flask, flash, redirect, render_template, request, session, url_for
from modules import forms
import pymysql
import getpass
# End Import's

app = Flask(__name__)
app.secret_key = 'Any String or Number for encryption here'
title = 'InternREQ-'

# Temp
IP = '35.196.126.63'


@app.route('/')
def landing():
    return render_template('landingPage.html', title=title+"-Home")

# This method will eventually post credentials to databse
# -->Credential's fail: push error message
# -->Credential's pass: push user's dash


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.Login()
    if(form.validate_on_submit()):
        email = form.email.data
        pwrd = form.password.data
        pas = getpass.getpass('Enter Password: ')
        db = pymysql.connect(host=IP, user='root',
                             password=pas, db='internreq')
        c = db.cursor()
        c.execute('Select * from users where email="' +
                  email+'"')
        l = c.fetchall()  # With this tuple we can parse for information to assign each user
        db.close()

        if(len(l) != 0 and l[0][1] == email and l[0][2] == pwrd):
            session['Username'] = email
            route = '/dashboard/' + email
            return redirect(route)
        else:
            flash('Username or Password Error', 'danger')
    return render_template('login.html', title=(title + 'Login'), form=form)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = forms.Registration()
    if(form.validate_on_submit()):
        flash('Account Creation Successful!', 'success')
        return redirect('/login')
    return render_template('registration.html', title=(title+"-Registration"), form=form)


# START: Temporary code for testing how to foward based on user input
'''
    This code will eventually turn into a connection to the database when a user presses login from login html.
    
    When the login button is pushed and the form is submited the dashboard() function is called to route user to
        the appropriate page based on what WILL be returned from the user_type column in or database.
'''


@app.route('/profile/<user>')
def profile(user):
    if(session['Username'] == user):
        return (render_template('profile.html', Username=user, title=(title+"-Profile")))
    session.pop('Username', None)
    return redirect('/login')


# END: Temporary code for testing how to foward based on user input

'''
Based on the user_type returned from database query:
 foward user to appropriate dashboard
'''


@app.route('/dashboard/<name>')
def dashboard(name):
    if(session['Username'] == name):
        return render_template('dashboard.html', title=(title+'Dashboard'), Username=name)
    session.pop('Username', None)
    return redirect('/')


if (__name__ == "__main__"):
    app.run(host='0.0.0.0', port=8080, debug=True)
