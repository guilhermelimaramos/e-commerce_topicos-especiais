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
  

@app.route('/')
def page_home():
  return render_template('home.html')

@app.route('/products')
def page_products():
  itens = [
    {'id': 1, 'name': 'Phone', 'bar_code': '453462662', 'price': 1600},
    {'id': 2, 'name': 'Notebook', 'bar_code': '985342798', 'price': 3500},
    {'id': 3, 'name': 'Keyboard', 'bar_code': '187856781', 'price': 80},
    {'id': 4, 'name': 'Monitor', 'bar_code': '175981653', 'price': 2000}
  ]
  return render_template('products.html', itens=itens)

