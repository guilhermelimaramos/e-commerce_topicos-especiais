from commerce import app
from flask import render_template, redirect, url_for, flash, request
from commerce.models import Product, User
from commerce.forms import SignUpForm, SignInForm, BuyProductForm, SellProductForm
from commerce import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
def page_home():
  return render_template('home.html')

@app.route('/products', methods=['GET', 'POST'])
@login_required
def page_products():
  buy_form = BuyProductForm()
  if request.method == 'POST':
    buy_product = request.form.get('buy_product')
    prod_obj = Product.query.filter_by(name=buy_product).first()
    print(prod_obj.owner)
    if prod_obj:
      prod_obj.owner = current_user.id
      current_user.balance -= prod_obj.price
      db.session.commit()
      flash(f'Congratulations! You bought {prod_obj.name} for R$ {prod_obj.price}', category='success')
    return redirect(url_for('page_products'))
  product = Product.query.all()
  return render_template('products.html', product=product, buy_form=buy_form)

@app.route('/signup', methods=['GET', 'POST'])
def page_signup():
  form = SignUpForm()
  if form.validate_on_submit():
    new_user = User(
      username = form.username.data,
      email = form.email.data,
      pw_hash = form.password1.data
    )
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('page_products'))
  if form.errors != {}:
    for err in form.errors.values():
      flash(f"Error: {', '.join([str(e).replace('[', '').replace(']', '') for e in err])}", category="danger")
  return render_template('signup.html', form=form)

@app.route('/signin', methods=['GET', 'POST'])
def page_signin():
  form = SignInForm()
  if form.validate_on_submit():
    user_signin = User.query.filter_by(username=form.username.data).first()
    if user_signin and user_signin.pw_decript(pw_text=form.password.data):
      login_user(user_signin)
      flash(f'Welcome! {user_signin.username}', category='success')
      return redirect(url_for('page_products'))
    else: 
      flash(f'Error: incorrect username and/or password! Try again!', category='danger')
  return render_template('login.html', form=form)

@app.route('/logout')
def page_logout():
  logout_user()
  flash("You have logged out", category="info")
  return redirect(url_for('page_home'))