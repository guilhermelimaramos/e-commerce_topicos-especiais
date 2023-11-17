from commerce import app
from flask import render_template
from commerce.models.product import Product

@app.route('/')
def page_home():
  return render_template('home.html')

@app.route('/products')
def page_products():
  product = Product.query.all()
  return render_template('products.html', product=product)