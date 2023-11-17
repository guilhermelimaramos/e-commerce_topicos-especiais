from commerce import app
from flask import render_template
from commerce.models import Product
from forms import SignUpForm

@app.route('/')
def page_home():
  return render_template('home.html')

@app.route('/products')
def page_products():
  product = Product.query.all()
  return render_template('products.html', product=product)

@app.route('/signup')
def page_signup():
  form = SignUpForm()
  return render_template('signup.html', form=form)