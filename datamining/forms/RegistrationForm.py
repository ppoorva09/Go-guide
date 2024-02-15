from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=10)])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    userType = SelectField('Role', validators=[DataRequired()], choices=[('CUSTOMER', 'Customer')])
    submitRegistration = SubmitField('Sign Up')
