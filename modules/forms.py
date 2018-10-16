from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, StringField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class Login(FlaskForm):
    email = StringField('Email Address: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    save = BooleanField('Remeber Me')
    submit = SubmitField('Login')


class Registration(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    user_type = SelectField('Account Type', validators=[DataRequired()], choices=[
                            ('stu', 'Student'), ('fac', 'Faculty'), ('spo', 'Sponsor')])
    v_key = StringField('Verification Key', validators=[DataRequired()])
    email = StringField('Email address', validators=[
                        DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6, max=15)])
    confirm = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
