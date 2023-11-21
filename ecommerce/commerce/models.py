from commerce import db
from commerce import bcrypt

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(length=30), nullable=False, unique=True)
  email = db.Column(db.String(length=50), nullable=False, unique=True)
  password = db.Column(db.String(length=50), nullable=False)
  balance = db.Column(db.Integer, nullable=False, default=5000) 
  products = db.relationship('Product', backref='owner_user', lazy=True)

  @property
  def pw_hash(self):
    return self.pw_hash

  @pw_hash.setter
  def pw_hash(self, pw_text):
    self.password = bcrypt.generate_password_hash(pw_text).decode('utf-8')

class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(length=30), nullable=False, unique=True)
  price = db.Column(db.Integer, nullable=False)
  bar_code = db.Column(db.String(length=12), nullable=False, unique=True)
  description = db.Column(db.String(length=1024), nullable=False)
  owner = db.Column(db.Integer, db.ForeignKey('user.id'))

def __repr__(self):
  return f"Product {self.name}"