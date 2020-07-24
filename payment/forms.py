from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class SignupForm(FlaskForm):
    Firstname = StringField('First Name', validators=[DataRequired()])
    Lastname = StringField('Last Name', validators=[DataRequired()])
    Username = StringField('User Name', validators=[DataRequired()])
    Email = StringField('Email Address', validators=[DataRequired(), Email()])
    Password = PasswordField('Enter Password', validators=[DataRequired()])
    Confirmpassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('Password')])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    Email = StringField('Email Address', validators=[DataRequired(), Email()])
    Password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class PaymentForm(FlaskForm):
    Email = StringField('Email Address', validators=[DataRequired(), Email()])
    Cardnumber = IntegerField('Credit Card Number', validators=[DataRequired()])
    Expiry = DateField('Year of expiry', validators=[DataRequired()])
    Cvc = IntegerField('CVC', validators=[DataRequired()])
    amounttopay = IntegerField('Amount to pay', validators=[DataRequired()])
    submit = SubmitField('Pay')
