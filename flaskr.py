'''Flask server to handle routing for InternREQ.com. '''

'''
Authors:
    Tom Birmingham
    Christopher Conlon
    Daniel G.
    Davis Jaekle
    Mohamad M.
'''
# Import's
from flask import Flask, render_template, redirect, url_for, request
# End Import's

app = Flask(__name__)
title = 'InternREQ-'


@app.route('/')
def landing():
    return render_template('landingPage.html', title=title+"-Home")


@app.route('/login')
def login():
    return render_template('login.html', title=(title + "-Login"))

# This method will eventually post credentials to databse
# -->Credential's fail: push error message
# -->Credential's pass: push user's dash


@app.route('/login', methods=['POST'])
def login_foward():
    user = request.form['Username']
    route = '/dashboard/' + user
    return redirect(route)


@app.route('/registration')
def registration():
    return render_template('registration.html', title=(title+"-Registration"))


@app.route('/registration', methods=['POST'])
def registrationPost():
    # All variables must be checked against database and be INSERT'ed into...
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    user = request.form['User']
    verify = request.form['verificationKey']
    pswrd = request.form['password']
    confirm = request.form['re-enter']
    email = request.form['Email']

    if(pswrd != confirm):
        return (render_template('registration.html', title=(title+'-Login')) + "<script>alert('Passwords do not match');</script>")

    return ("<h1>" + firstName + " " + lastName + " " + user + " " + verify + " " + email + " " + pswrd + " " + confirm + " " + "</h1>")


# START: Temporary code for testing how to foward based on user input
'''
    This code will eventually turn into a connection to the database when a user presses login from login html.
    
    When the login button is pushed and the form is submited the dashboard() function is called to route user to
        the appropriate page based on what WILL be returned from the user_type column in or database.
'''


@app.route('/profile/<user>')
def foward_dash(user):
    return (render_template('profile.html', username=user, title=(title+"-Profile")))


# END: Temporary code for testing how to foward based on user input

'''
Based on the user_type returned from database query:
 foward user to appropriate dashboard
'''


@app.route('/dashboard/<name>')
def dashboard(name):
    user = name
    return render_template('dashboard.html', title=(title+'Dashboard'), Username=user)

# START: Test route will be removed at time of product release


@app.route('/test')
def test():
    return render_template('dashboard.html', title=(title+'Dash'))

# End: Test route will be removed at time of product release


if (__name__ == "__main__"):
    app.run(host='0.0.0.0', port=8080, debug=True)
