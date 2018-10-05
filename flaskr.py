from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


@app.route('/')
def landing():
    return render_template('landingPage.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/registration')
def registration():
    return render_template('registration.html')


@app.route('/registration', methods=['POST'])
def registrationPost():
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    user = request.form['User']
    verify = request.form['verificationKey']
    pswrd = request.form['password']
    confirm = request.form['re-enter']
    email = request.form['Email']

    if(pswrd != confirm):
        # from the plus sign on we need to append a <style> tag to target the form and make sure specific things
        # match
        return (render_template('registration.html') + "<h1>Password missmatch</h1>")

    return ("<h1>" + firstName + " " + lastName + " " + user + " " + verify + " " + pswrd + " " + confirm + " " + email + "</h1>")


# START: Temporary code for testing how to foward based on user input
'''
    This code will eventually turn into a connection to the database when a user presses login from login html.
    
    When the login button is pushed and the form is submited the dashboard() function is called to route user to
        the appropriate page based on what WILL be returned from the user_type column in or database.
'''


@app.route('/dashboard')
def foward_dash():
    return ('<form action="" method="POST"><input<label>Student <input type="radio" name="user" value="Student"></label></br>'
            '<label>Faculty: <input type="radio" name="user" value="Faculty"></label></br>'
            '<label>Employer: <input type="radio" name="user" value="Sponsor"></label></form></br>'
            '<button type="submit">Submit</button>')


# END: Temporary code for testing how to foward based on user input


@app.route('/dashboard', methods=['POST'])
def dashboard():
    user_type = request.form['user']
    if(user_type == 'Faculty'):
        return ('<h1>Admin dashboard</h1>')

    elif(user_type == 'Sponsor'):
        return ('<h1>Sponsor dashboard</h1>')

    elif(user_type == 'Student'):
        return '<h1>Student dashboard</h1>'


if (__name__ == "__main__"):
    app.run(host='0.0.0.0', port=8080, debug=True)
