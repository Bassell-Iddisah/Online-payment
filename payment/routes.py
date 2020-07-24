from flask import Flask, jsonify, render_template, request, url_for
from payment import app, db
from payment.forms import SignupForm, LoginForm, PaymentForm
import stripe
import os


stripe_keys = {
  'secret_key': os.environ['SECRET_KEY'],
  'publishable_key': os.environ['TEST_KEY']
}

stripe.api_key = stripe_keys['secret_key']



def index():
    form = PaymentForm()
    if form.validate_on_submit():
        pass
    return render_template('index.html', key=stripe_keys['publishable_key'], form=form)


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def login():
    logform = LoginForm()
    if logform.validate_on_submit():
        pass
    return render_template('login.html', form=logform)


@app.route('/register', methods=['GET', 'POST'])
def register():
    regform = LoginForm()
    if regform.validate_on_submit():
        pass
    return render_template('register.html', form=regform)


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
