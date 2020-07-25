from flask import Flask, jsonify, render_template, request, url_for, flash, redirect
from payment import app, db, bcrypt
from payment.forms import SignupForm, LoginForm, PaymentForm
from payment.models import Student
from flask_login import login_user
import stripe
import os


stripe_keys = {
  'secret_key': os.environ['SECRET_KEY'],
  'publishable_key': os.environ['TEST_KEY']
}

stripe.api_key = stripe_keys['secret_key']


@app.route('/fee_paying')
def index():
    form = PaymentForm()
    if form.validate_on_submit():
        pass
    return render_template('index.html', key=stripe_keys['publishable_key'], form=form)


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    logform = LoginForm()
    if logform.validate_on_submit():
        email = logform.Email.data
        student = Student.query.filter_by(email=email).first()
        if student and bcrypt.check_password_hash(student.password, logform.Password.data):
            login_user(student)
            flash(f'{student.username} login successful', 'success')
            return redirect(url_for('index'))
    return render_template('login.html', form=logform)


@app.route('/register', methods=['GET', 'POST'])
def register():
    regform = SignupForm()
    if regform.validate_on_submit():
        firstname = regform.Firstname.data
        lastname = regform.Lastname.data
        username = regform.Username.data
        email = regform.Email.data
        password = bcrypt.generate_password_hash(regform.Password.data)
        new_student = Student(firstname=firstname, lastname=lastname,
                              username=username, email=email, password=password)
        db.session.add(new_student)
        db.session.commit()
        flash(f'Account for {new_student.firstname} created successfully, Please login to continue.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', legend='Register', form=regform)


@app.route('/charge', methods=['POST'])
def charge():
    form = PaymentForm()
    try:
        customer = stripe.Customer.create(
            email=form.email.data,
            source=request.json['token']
        )
        stripe.Charge.create(
            customer=customer.id,
            amount=form.amounttopay.data,
            currency='ghs',
            description=request.json['description']
        )
        return jsonify({'status': 'success!'})
    except stripe.error.StripeError:
        return jsonify({'status': 'error'}), 500
