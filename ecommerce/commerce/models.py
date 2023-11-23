from commerce import db, login_manager
from commerce import bcrypt
from flask_login import UserMixin

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
  
  def purchase_available(self, item_obj):
    return self.balance >= item_obj.price
  
  def sell_available(self, item_obj):
    return self.id == item_obj.owner
  
  def change_username(self, new_username):
    self.username = new_username
    db.session.commit()
  
class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(length=30), nullable=False, unique=True)
  price = db.Column(db.Integer, nullable=False)
  bar_code = db.Column(db.String(length=12), nullable=False, unique=True)
  description = db.Column(db.String(length=1024), nullable=False)
  owner = db.Column(db.Integer, db.ForeignKey('user.id'))

  def __repr__(self):
    return f"Product {self.name}"

  def purchase(self, user):
    self.owner = user.id
    user.balance -= self.price
    db.session.commit()
  
  def sell(self, user):
    self.owner = None
    user.balance += self.price
    db.session.commit()