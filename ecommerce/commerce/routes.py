from commerce import app
from flask import render_template, redirect, url_for
from commerce.models import Product, User
from commerce.forms import SignUpForm
from commerce import db

@app.route('/')
def page_home():
  return render_template('home.html')

@app.route('/products')
def page_products():
  product = Product.query.all()
  return render_template('products.html', product=product)

@app.route('/signup', methods=['GET', 'POST'])
def page_signup():
  form = SignUpForm()
  if form.validate_on_submit():
    new_user = User(
      username = form.username.data,
      email = form.email.data,
      password = form.password1.data
    )
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('page_products'))
  
  return render_template('signup.html', form=form)