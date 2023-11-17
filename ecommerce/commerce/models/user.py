from commerce import db

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(length=30, nullable=False, unique=True))
  email = db.Column(db.String(length=50), nullable=False, unique=True)
  password = db.Column(db.String(length=50), nullable=False)
  balance = db.Column(db.Integer, nullable=False, default=5000) 
  products = db.relationship('Product', backref='owner_user', lazy=True)
