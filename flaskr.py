''' Flask server to handle routing for InternREQ.com. '''

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
# end Import's


# Globals
app_title = 'InternREQ'
app = Flask(__name__)
app.secret_key = 'Any String or Number for encryption here'

# Mail Configuration    <!> Set environment variable before testing locally
#       Windows (powershell):     $env:MAIL_PASS = 'ourpassword'
#       Winders (CMD):            set MAIL_PASS=ourpassword
#       Mac (Terminal):           export MAIL_PASS=ourpassword
app.config.update(dict(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME='chrisddhnt@gmail.com',
    MAIL_PASSWORD=os.environ.get('MAIL_PASS')
))
app.config.from_object(__name__)
mail = Mail(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

sessionID = []
serial = URLSafeTimedSerializer(app.secret_key)
ALLOWED_EXTENSIONS = set(['pdf'])

# Database Access   <!> Set environment variable before testing locally
#       Windows:   $env:DB_PASS = 'ourpassword'
#       Windows:   set DB_PASS=ourpassword
#       Mac:       export DB_PASS=ourpassword
db_ip = '35.221.39.35' #internreq database
db_password = os.environ.get('DB_PASS')
db_user = 'root'
db_name = 'internreq'
db_connection_name = 'birmingham4test:us-east4:internreq-1'

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
        self.department = row[4]
        self.major = row[4]
        self.company = row[4]
        self.location = row[5]
        self.about = row[6]
        self.url = row[7]
        self.phone = row[9]
        self.phone_desc = row[10]
        self.verified = row[11]
        self.education = row[12]
        self.additional = row[13]
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

        # additional datapoints
        if (self.role == 'student'):
            self.grad_date = row[14]
            self.gpa = row[15]
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
@app.errorhandler(404)
def page_not_found(a):
    # This route is for handling when an incorrect url is typed
    return render_template('404.html', title=app_title)
  
@app.errorhandler(500)
def server_error(b):
    # This route is for handling when an internal server error occurs
    return render_template('500.html', title=app_title)

@app.errorhandler(Exception)
def all_other_errors(c):
    # This route is for catching all non 404 or 500 errors
    return render_template('Exception.html', title=app_title)


# Landing Page Route 
@app.route('/')
def landing():
    if(current_user.is_authenticated):
        return redirect(url_for('dashboard'))
    return render_template('landingPage.html', title=app_title)


#   Login Page Route
#   This is the route for login page, when first opening the page it is opened
#   via a GET request and ONLY the last render template executes.
#   If the user clicks submit the POST method executes and server recives entered data and verifies
#   against the database
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
                return(render_template('login.html', title=app_title, form=form))
        else:
            flash('Username or Password Error', 'danger')
    return render_template('login.html', title='Login | '+app_title, form=form)


#   Logout Route
@app.route('/logout')
def logout():
    logout_user()
    flash('Logout Successfull', 'success')
    return redirect(url_for('login'))

#   Registration Page Route
#   Same as Login: only last line executes at first, upon submit the if statment executes and evaluates
#   against our database. If account not in database: create a new user
#                         Else: foward to login page and request user to login
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = forms.Registration()

    if(form.validate_on_submit()):
        # Retreive inputs
        first = form.first_name.data
        last = form.last_name.data
        user_type = form.user_type.data
        email = form.email.data
        pswrd = form.confirm.data
        pswrd = db.encrypt(pswrd)

        # Pull from Database
        sql = "SELECT * FROM users WHERE email LIKE '%s'" % email

        if(len(db.query('PULL', sql)) == 0):
            sql = "INSERT INTO users (user_id, email, password, role, name) VALUES (%s,%s,%s,%s,%s)"
            args = (0, email, pswrd, user_type, first)
            db.query('PUSH', sql, args)
            # add to sudent/faculty/sponsor table
            sql = "SELECT user_id FROM users WHERE email LIKE '%s'" % email
            user_id = db.query("PULL", sql)[0][0]
            sql = "INSERT INTO "+user_type+" (user_id, first_name, last_name, email, verified) VALUES(%s,%s,%s,%s,%s)"
            args = (user_id, first, last, email, 0)
            db.query('PUSH', sql, args)

            # Check if it is southern email address
            southern = email.split('@')
            if(southern[1] == 'southernct.edu'):
                token = serial.dumps(email, salt='email-confirm')
                msg = Message(sender='chrisddhnt@gmail.com',subject="Email Verification", recipients=[email])
                link = (url_for('email_confirm', token=token, _external=True))
                msg.body = (
                    'Thanks for signing up. Here is your registration key \n{}').format(link)
                mail.send(msg)
            else:
                msg = Message(sender='chrisddhnt@gmail.com',subject="User Verification", recipients=['chris.conlon1993@gmail.com'])
                link = (url_for('login', _external=True))
                msg.body = ('New Account created for Faculty/Sponsor. Do You want to allow user with email address {} into the system? If yes please login here {} and go to the appropriate page. Else discard this message').format(email,link)
                mail.send(msg)

        else:
            flash("Email address already used! Please Login.", 'danger')
            return redirect(url_for('registration'))

        flash('Account Creation Successful!', 'success')
        return redirect('/login')

    return render_template('registration.html', title='Registration | '+app_title, form=form)


#   Email Confirmation Route 
@app.route('/email_confirm/<token>')
def email_confirm(token):
    try:
        email = serial.loads(token, salt='email-confirm', max_age=3600)# token lives for 1 hour
        student = db.query('PULL', "Select user_id FROM users WHERE email='{}'".format(email))
        db.query('PUSH', "UPDATE student SET verified=TRUE WHERE user_id={}".format(student[0][0]))
    except Exception:
        flash('Your verification link has expired please re-register')
        return redirect('/scoobysnacks')
    flash('Account Verified!')
    return(redirect(url_for('login')))


#   User Confirmation Route    
@app.route('/user_confirm', methods=['GET', 'POST'])
def user_confirm():
    if(not(current_user.is_authenticated) or current_user.role != 'faculty'):
        return render_template('unauthorized.html')
    else:
        form = forms.AddUser()
        if(form.validate_on_submit()):
            email = form.email.data
            sql = "SELECT * FROM users WHERE email='{}'".format(email)
            user = db.query('PULL', sql)
            if(len(user) != 0):
                user = user[0]
                sql = "UPDATE {} SET verified=True WHERE user_id={}".format(user[3], user[0]) # update <role_table> with a true value in verified 
                db.query('PUSH',sql)
                flash('User has been verified.', 'success')
            else:
                flash('No user with the email address is registered', 'danger')
            return(redirect(url_for('user_confirm', form=form)))
        return(render_template('AddUser.html', form=form))


#   Profile Page Route
@app.route('/profile/<user_id>', methods=['GET', 'POST'])
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
            return render_template('profile.html', title=page_title+app_title, profile_user=profile_user, Edit=edit, Privacy = privacy)
        else:
            # profile does not exist
            return render_template('404.html', title=app_title)
    else:
        return redirect('/login')


#   File Upload Route (for uploading resume)
@app.route('/upload_file', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'inputFile' not in request.files:
            flash('No file part')
            return redirect(url_for('profile', user_id=current_user.id))
        file = request.files['inputFile']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('profile', user_id=current_user.id))
        if file and allowed_file(file.filename):
            data = file.read()
            args = (data, current_user.id)
            sql = 'UPDATE student SET resume = %s WHERE user_id = %s'
            db.query("PUSH", sql, args)
            flash('File uploaded successfully', 'success')
            return redirect(url_for('profile', user_id=current_user.id))
    return redirect(url_for('landing'))

# helper function if file is allowed (Boolean)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#   Edit Profile Route
#   This is the code for editing profile. The user is presented the data currently
#   linked to their account and is able to edit these values and have the changes
#   reflected in their profile page
@app.route('/profile/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user_id = current_user.id
    if db.query("PULL", "SELECT role FROM users WHERE user_id = %s" % (user_id)): 
        if(current_user.role == 'faculty'):
                form = forms.EditProfileF()
        elif(current_user.role == 'sponsor'):
                form = forms.EditProfileSp()
        else:
                form = forms.EditProfileS()
        if (request.method == 'GET'):
            if(current_user.role == 'faculty'):
                sql = "SELECT first_name, last_name, title, department, location, about, private FROM faculty WHERE user_id = %s" % (user_id)
                first_name, last_name, user_title, department, location, about, private = db.query('PULL', sql)[0]
                form.first_name.data, form.last_name.data, form.user_title.data, form.department.data, form.location.data, form.about.data, form.private.data = first_name, last_name, user_title, department, location, about, private
                return render_template('edit_profilef.html', title='Edit Profile', form=form)

            elif(current_user.role == 'student'):
                sql = "SELECT first_name, last_name, title, major, location, about, education, additional, graduation_date, GPA, private FROM student WHERE user_id = %s" % (user_id)
                first_name, last_name, user_title, major, location, about, education, skills, grad_date, gpa, private = db.query('PULL', sql)[0]
                form.first_name.data, form.last_name.data, form.user_title.data, form.major.data, form.location.data, form.about.data, form.education.data, form.skills.data, form.grad_date.data, form.gpa.data, form.private.data = first_name, last_name, user_title, major, location, about, education, skills, grad_date, gpa, private
                return render_template('edit_profiles.html', title='Edit Profile', form=form, first_name = first_name, user_title=user_title, major = major, location=location, about=about, education=education, skills=skills, grad_date = grad_date, gpa=gpa, private=private)

            elif(current_user.role == 'sponsor'):
                sql = "SELECT first_name, last_name, title, company, about, education, additional, private FROM sponsor WHERE user_id =  %s" % (user_id)
                first_name, last_name, user_title, company, about, education, skills, private = db.query('PULL', sql)[0]
                form.first_name.data, form.last_name.data, form.user_title.data, form.company.data, form.about.data, form.education.data, form.skills.data, form.private.data = first_name, last_name, user_title, company, about, education, skills, private
                return render_template('edit_profilesp.html', title='Edit Profile', form=form, first_name = first_name, last_name = last_name, user_title = user_title, company = company, about=about, education=education, skills=skills, private=private)
        else:
            if(current_user.role == 'faculty'):
                new_private = str(form.private.data)
                if(new_private is 'True'):
                    flag = True
                else:
                    flag = False
                sql = "UPDATE faculty SET first_name = '%s', last_name = '%s', title = '%s', department = '%s', location = '%s', about = '%s', private = %s WHERE user_id = %s" % (form.first_name.data, form.last_name.data, form.user_title.data, form.department.data, form.location.data, form.about.data, flag, user_id)
                db.engine.execute(sql)
                return redirect(url_for('profile', user_id=current_user.id))
            elif(current_user.role == 'student'):
                new_private = str(form.private.data)
                if(new_private is 'True'):
                    flag = True
                else:
                    flag = False
                sql = "UPDATE student SET first_name = '%s', last_name= '%s', title = '%s', major = '%s', location = '%s', about = '%s', education = '%s', additional = '%s', graduation_date = '%s', gpa = '%s', private = %s WHERE user_id = %s" % (form.first_name.data, form.last_name.data, form.user_title.data, form.major.data, form.location.data, form.about.data, form.education.data, form.skills.data, form.grad_date.data, form.gpa.data, flag, user_id)
                db.engine.execute(sql)            
                return redirect(url_for('profile', user_id=current_user.id))
            elif(current_user.role == 'sponsor'):
                new_private = str(form.private.data)
                if(new_private is 'True'):
                    flag = True
                else:
                    flag = False
                sql = "UPDATE sponsor SET first_name = '%s', last_name = '%s', title = '%s', company = '%s', about = '%s', education = '%s', additional = '%s', private = %s WHERE user_id = %s" % (form.first_name.data, form.last_name.data, form.user_title.data, form.company.data, form.about.data, form.education.data, form.skills.data, flag, user_id)
                db.engine.execute(sql)
                return redirect(url_for('profile', user_id=current_user.id))


@app.route('/testinghtml')
def testing():
    return render_template('testing.html')

# Route for Help Page
@app.route('/help')
def help():
    return render_template('help.html', title='Help| InternREQ')

#   Dashboard Page Route
@app.route('/dashboard')
@login_required
def dashboard():
    if(current_user.is_authenticated):
        name = current_user.name
        postings = db.query('PULL', 'SELECT * FROM internship')
        applications = []
        applicants=""
        user_id = str(current_user.id)
        if(current_user.role == 'student'):
            posting = db.query('PULL', 'SELECT * FROM applications WHERE student_id =' + user_id)
            for x in range(len(posting)):
                applications.append(db.query(
                    'PULL', 'SELECT * FROM internship WHERE internship_id={}'.format(posting[x][2]))[0])
        elif(current_user.role == 'sponsor'):
            applicants = db.query('PULL', "SELECT last_name, first_name, major, graduation_date,user_id FROM student s INNER JOIN applications a ON s.user_id = a.student_id WHERE a.sponsor_id = {}".format(current_user.id))
            posting = db.query('PULL', 'SELECT * FROM internship WHERE sponsor_id=' + user_id)
            for x in range(len(posting)):
                applications.append(db.query(
                    'PULL', 'SELECT * FROM internship WHERE sponsor_id={}'.format(posting[x][1]))[0])



        return render_template('dashboard.html', title=('Dashboard | '+app_title), applied=applications, name=name, Daily="Welcome to the Program", postings=postings ,applicants = applicants)
    return redirect('/login')


#   Internship Posting Page Route
@app.route('/posting/<id>', methods=['GET', 'POST'])
def posting(id):

    # Apply Now button -- add a case if the user has already applied, flash success you have already applied
    if request.method == 'POST':
        # check if user already has an application
        sql = 'SELECT * FROM applications WHERE student_id = %s AND internship_id = %s' % (current_user.id, id)
        result = db.query('PULL', sql)
        if result:
            flash('Application Already Submitted', 'success')
        # else add and entry to the applications table
        else:
            sql = 'SELECT sponsor_id FROM internship WHERE internship_id = %s' % (id)
            sponsor_id = db.query('PULL', sql)[0][0]
            sql = 'INSERT INTO applications (student_id, internship_id, sponsor_id) VALUES(%s,%s,%s)'
            args = (current_user.id, id, sponsor_id)
            db.query('PUSH', sql, args)
            flash('Application Submited', 'success')
    # when loading posting we do not need the ID or user ID so start at title and go from there ([0][3:])
    posting = db.query(
        'PULL', "SELECT * FROM internship WHERE internship_id="+id)[0][3:]
    post_title = posting[0]
    post_type = posting[6]
    page_title = post_title+' - '+post_type+' | '
    return render_template('posting.html', title=page_title+app_title, datePosted=1, postingInfo=posting)


#   Create Internship Listing/Posting Route
@app.route('/create/posting', methods=['GET', 'POST'])
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
            sql = "INSERT INTO internship(internship_id, sponsor_id, title," \
                " location, overview, responsibilities, requirements, compensation, type, availability)VALUES"\
                "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            args = (0, current_user.id, title, location,
                    overview, repsons, reqs, comp, jType, hours)
            db.query('PUSH', sql, args)
            return redirect('/profile/'+str(current_user.id))
        return(render_template('posting.html', title='Create Posting | '+app_title, form=form))
    return(render_template('unauthorized.html'))


#   Send Mail Route
def send_email(subject, sender, recipients, body):
    msg = Message(subject, sender=sender, recipients=[recipients])
    msg.html = body
    mail.send(msg)


#   Admin Tables View Route
@app.route('/admin_view')
@login_required
def admin_view():
    userTable = db.query('PULL', "Select * from users")
    studentTable = db.query('PULL', "Select * from student")
    sponsorTable = db.query('PULL', "Select * from sponsor")
    facultyTable = db.query('PULL', "Select * from faculty")
    return render_template('adminView.html', title='Administration | '+app_title, users=userTable,students=studentTable,sponsors=sponsorTable, facultyM=facultyTable)


#   Users Search Route
@app.route('/results/<user_search>')
def general_search(user_search):
    user_results = db.query('PULL', "SELECT * from users WHERE name LIKE '%%{}%%'".format(user_search))
    student_results = db.query('PULL', "SELECT * from student WHERE first_name LIKE '%%{}%%'".format(user_search))
    sponsor_results = db.query('PULL', "Select * from sponsor WHERE company LIKE '%%{}%%'".format(user_search))
    faculty_results = db.query('PULL', "Select * from faculty WHERE first_name LIKE '%%{}%%'".format(user_search))
    internship_results = db.query('PULL', "Select * from internship t1 INNER JOIN sponsor t2 ON t1.sponsor_id=t2.user_id WHERE t1.title LIKE '%%{}%%'".format(user_search))
    return render_template('searchResults.html', users=user_results, students=student_results, sponsors=sponsor_results, faculty=faculty_results, internships=internship_results, title='Results For "'+user_search+'"')


#   Search Helper Route
@app.route('/search_handler',methods=['POST'])
def search_handler():
    search = request.form['searchingFor']
    if('%20' in search):
        search.replace('%20', " ")
    return (redirect( url_for("general_search", user_search=search) ))


if (__name__ == "__main__"):
    if os.environ.get('GAE_ENV') != 'standard': # if not deployed to the app engine
        app.run(host='0.0.0.0', port='8080', debug=True)
