from commerce import db, login_manager
from commerce import bcrypt
from flask_login import UserMixin
from sqlalchemy import Enum

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(length=30), nullable=False, unique=True)
  email = db.Column(db.String(length=50), nullable=False, unique=True)
  password = db.Column(db.String(length=50), nullable=False)
  balance = db.Column(db.Integer, nullable=False, default=5000) 
  products = db.relationship('Product', backref='owner_user', lazy=True)

  @property
  def format_balance(self):
    if len(str(self.balance)) >= 4:
      return f"R$ {str(self.balance)[:-3]}, {str(self.balance)[-3:]}"
    else:
      return f"R$ {self.balance}"
  
  @property
  def pw_hash(self):
    return self.pw_hash

  @pw_hash.setter
  def pw_hash(self, pw_text):
    self.password = bcrypt.generate_password_hash(pw_text).decode('utf-8')
  
  def pw_decript(self, pw_text):
    return bcrypt.check_password_hash(self.password, pw_text)
  
  def purchase_available(user, subtotal):
    return user.balance >= subtotal
  
  def sell_available(self, item_obj):
    return self.id == item_obj.owner
  
  def change_username(self, new_username):
    self.username = new_username
    db.session.commit()
  
  def change_password(self, new_password):
    self.pw_hash = new_password
    db.session.commit()

  def delete_account(self):
    db.session.delete(self)
    db.session.commit()
  
class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(length=30), nullable=False, unique=True)
  price = db.Column(db.Integer, nullable=False)
  bar_code = db.Column(db.String(length=12), nullable=False, unique=True)
  description = db.Column(db.String(length=1024), nullable=False)
  status = db.Column(Enum('available', 'cart', 'sold', name='status'), nullable=False, default='available')
  owner = db.Column(db.Integer, db.ForeignKey('user.id'))

  def __repr__(self):
    return f"Product {self.name}"

  def purchase(user, subtotal):
    user.balance -= subtotal
    db.session.commit()
  
  def sell(self, user):
    self.owner = None
    user.balance += self.price
    db.session.commit()

  def add_cart(self, user):
    self.status = 'cart'
    self.owner = user.id
    db.session.commit()
  
  def subtotal(self, user): 
    for product in Product.query.filter_by(owner=user.id):
      return sum(product.price)

  def complete_purchase(self):
    self.status = 'sold'
    db.session.commit()  

  def remove_all_cart(self):
    self.status = 'available'
    self.owner = None
    db.session.commit()
  