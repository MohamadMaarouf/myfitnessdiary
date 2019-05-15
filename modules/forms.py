from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, BooleanField, DateField, IntegerField
from datetime import date
from wtforms.validators import DataRequired, Email, Length, EqualTo

application_title = 'MyFitnessDiary'
application = Flask(__name__)

class Login(FlaskForm):
    email = StringField('Email: ', validators=[DataRequired(), Email()])
    password = PasswordField('Password: ', validators=[
                             DataRequired(), Length(min=6, max=255)])
    submit = SubmitField('Login')


class Registration(FlaskForm):
    first_name = StringField('First Name: ', validators=[DataRequired()])
    last_name = StringField('Last Name: ', validators=[DataRequired()])
    email = StringField('Email: ', validators=[DataRequired(), Email()])
    password = PasswordField('Password: ', validators=[
        DataRequired(), Length(min=6)])
    confirm = PasswordField('Confirm Password:  ', validators=[
        DataRequired(), EqualTo('password')])
    submit = SubmitField('Register ', validators=[DataRequired()])

class EditProfileM(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    user_title = StringField('Caption', validators=[Length(min=0, max=50)])   
    location = StringField('Gym Location', validators = [Length(min=0, max = 50)])
    about = TextAreaField('About', validators=[Length(min=0, max=255)])
    goalWeight = StringField('Goal Weight:', validators=[DataRequired()])    
    mainExercise = SelectField('Exercise',
                           validators=[DataRequired()],
                           choices=[('Benchpress', 'Benchpress'), ('Deadlift', 'Deadlift'), ('Squat', 'Squat')])
    workoutOne = SelectField('Exercise One', validators=[DataRequired()], choices = [('Incline Dumbbell Press', 'Incline Dumbbell Press'), ('Incline Benchpress', 'Incline Benchpress'),('Flat Dumbbell Press', 'Flat Dumbbell Press'), ('Chest flies', 'Chest flies'), ('Pushups', 'Pushups'), ('Chest Dips', 'Chest Dips'), ('Leg Extensions', 'Leg Extensions'), ('Hamstring Curls', 'Hamstring Curls'), ('Leg Press', 'Leg Press'), ('Lat Pulldowns', 'Lat Pulldowns'), ('Barbell Rows','Barbell Rows'), ('Back Pull Machine', 'Back Pull Machine')])
    workoutTwo = SelectField('Exercise Two', validators=[DataRequired()], choices = [('Incline Dumbbell Press', 'Incline Dumbbell Press'), ('Incline Benchpress', 'Incline Benchpress'),('Flat Dumbbell Press', 'Flat Dumbbell Press'), ('Chest flies', 'Chest flies'), ('Pushups', 'Pushups'), ('Chest Dips', 'Chest Dips'), ('Leg Extensions', 'Leg Extensions'), ('Hamstring Curls', 'Hamstring Curls'), ('Leg Press', 'Leg Press'), ('Lat Pulldowns', 'Lat Pulldowns'), ('Barbell Rows','Barbell Rows'), ('Back Pull Machine', 'Back Pull Machine')])
    workoutThree = SelectField('Exercise Three', validators=[DataRequired()], choices = [('Incline Dumbbell Press', 'Incline Dumbbell Press'), ('Incline Benchpress', 'Incline Benchpress'),('Flat Dumbbell Press', 'Flat Dumbbell Press'), ('Chest flies', 'Chest flies'), ('Pushups', 'Pushups'), ('Chest Dips', 'Chest Dips'), ('Leg Extensions', 'Leg Extensions'), ('Hamstring Curls', 'Hamstring Curls'), ('Leg Press', 'Leg Press'), ('Lat Pulldowns', 'Lat Pulldowns'), ('Barbell Rows','Barbell Rows'), ('Back Pull Machine', 'Back Pull Machine')])
    url = StringField('Email', validators=[Length(min=0, max=100)])
    private = BooleanField('Private')
    submit = SubmitField('Submit')

class Posting(FlaskForm):
    dateOfPost = DateField('Date (yyyy-mm-dd)', validators=[DataRequired()], format='%Y-%m-%d')
    exercise = SelectField('Exercise',
                           validators=[DataRequired()], choices=[('Benchpress', 'Benchpress'), ('Deadlift', 'Deadlift'), ('Squat', 'Squat')])
    overview = TextAreaField('Overview', validators=[])
    current = TextAreaField('Current Weight Max', validators=[])
    goal = TextAreaField('Goal Weight Max', validators=[])

    '''
    Put more fields here
    '''

    submit = SubmitField('Create Posting ', validators=[DataRequired()])

class graphOptions(FlaskForm):
    exercise = SelectField('Exercise', validators=[DataRequired()], choices=[('Benchpress', 'Benchpress'), ('Deadlift', 'Deadlift'), ('Squat', 'Squat')])
    timeScale = SelectField('Time Scale', validators=[DataRequired()], choices=[('Year', 'Year'), ('Month', 'Month'), ('Day', 'Day')])
    submit = SubmitField('Generate Graph', validators=[DataRequired()])
