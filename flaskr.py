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
    user = request.form['user']
    verify = request.form['verificationKey']
    pswrd = request.form['password']
    confirm = request.form['re-enter']
    email = request.form['Email']

    if(pswrd != confirm):
        # from the plus sign on we need to append a <style> tag to target the form and make sure specific things
        # match
        return (render_template('registration.html') + "<h1>PAss mis</h1>")

    return ("<h1>" + firstName + " " + lastName + " " + user + " " + verify + " " + pswrd + " " + confirm + " " + email + "</h1>")


if (__name__ == "__main__"):
    app.run(host='0.0.0.0', port=8080, debug=True)
