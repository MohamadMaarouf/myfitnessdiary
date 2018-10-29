''' Flask server to handle routing for InternREQ.com. '''

# Import's
import getpass
from modules import forms, Database
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
        first = form.first_name.data
        last = form.last_name.data
        user_type = form.user_type.data
        vKey = form.v_key.data
        email = form.email.data
        pswrd = form.confirm.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        # Pull from Database

        sql = 'Select * from users where email="' + email+'"'

        if(len(db.query('PULL', sql)) == 0):
            db.register(first, last, user_type, vKey, email, pswrd)
            print(db.query('PULL', "Select * from users"))
          
        '''db = pymysql.connect(host=IP, user='root',
                             password=pas, db='internreq')
        c = db.cursor()
        c.execute('Select * from users where email="' +
                  email+'"')
        l = c.fetchall()  # With this tuple we can parse for information to assign each user
        # ((1, 'chris.conlon1993@gmail.com', 'password', 'faculty admin'),)

        if(len(l) == 0):
            sql = "INSERT INTO users (user_id, email, password, role) VALUES(%s,%s,%s,%s)"
            c.execute(sql, (int(0), email, pswrd, user_type))
            c.execute("Select * from users")
            print(c.fetchall())

            # insert to student, faculty, sponsor tables
            sql = "SELECT user_id FROM users WHERE email LIKE '"+email+"'"
            c.execute(sql)
            user_id = c.fetchall()
            sql = "INSERT INTO "+user_type+"(user_id, first_name, last_name) VALUES(%s,%s,%s)"
            c.execute(sql, (user_id, first_name, last_name))'''
        
        else:
            flash("Email address already used! Please Login.", 'danger')
            return redirect('/registration')
        
        flash('Account Creation Successful!', 'success')
        db.commit()
        db.close()
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
