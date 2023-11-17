from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///market.db"
db.init_app(app)

class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(length=30), nullable=False, unique=True)
  price = db.Column(db.Integer, nullable=False)
  bar_code = db.Column(db.String(length=12), nullable=False, unique=True)
  description = db.Column(db.String(length=1024), nullable=False)

def __repr__(self):
  return f"Product {self.name}"
  

@app.route('/')
def page_home():
  return render_template('home.html')

@app.route('/products')
def page_products():
  product = Product.query.all()
  return render_template('products.html', product=product)

