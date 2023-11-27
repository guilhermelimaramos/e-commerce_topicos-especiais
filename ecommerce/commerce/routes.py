from commerce import app
from flask import render_template, redirect, url_for, flash, request
from commerce.models import Product, User
from commerce.forms import SignUpForm, SignInForm, BuyProductForm, SellProductForm, ChangeUsernameForm, ChangePasswordForm, AddCartForm
from commerce import db
from flask_login import login_user, logout_user, login_required, current_user

@app.context_processor
def inject_products():
    product = Product.query.filter_by(owner=None)
    owner_products = None
    if current_user.is_authenticated:
        owner_products = Product.query.filter_by(owner=current_user.id)
    return dict(product=product, owner_products=owner_products)

@app.route('/')
def page_home():
  return render_template('home.html')

@app.route('/products', methods=['GET', 'POST'])
@login_required
def page_products():
  buy_form = BuyProductForm()
  sell_form = SellProductForm()
  add_cart_form = AddCartForm()
  if request.method == 'POST':
    # Buy product
    # buy_product = request.form.get('buy_product')
    # prod_obj = Product.query.filter_by(name=buy_product).first()
    # if prod_obj:
    #   if current_user.purchase_available(prod_obj):
    #     prod_obj.purchase(user=current_user)
    #     flash(f'Congratulations! You bought {prod_obj.name} for R$ {prod_obj.price}', category='success')
    #   else:
    #     flash(f'Error: insufficient balance to buy {prod_obj.name}!', category='danger')
    # Sell product
    sell_product = request.form.get('sell_product')
    prod_obj_sell = Product.query.filter_by(name=sell_product).first()
    if prod_obj_sell:
      if current_user.sell_available(prod_obj_sell):
        prod_obj_sell.sell(user=current_user)
        flash(f'Congratulations! You sold {prod_obj_sell.name} for R$ {prod_obj_sell.price}', category='success')
      else:
        flash(f'Error: you cannot sell {prod_obj_sell.name}!', category='danger')
    # Add to cart
    add_cart_product = request.form.get('add_cart')
    prod_obj_add_cart = Product.query.filter_by(name=add_cart_product).first()
    if prod_obj_add_cart:
      prod_obj_add_cart.add_cart(user=current_user)
      flash(f'Congratulations! You added {prod_obj_add_cart.name} to your cart!', category='success')
    else:
      flash(f'Error: insufficient balance to add {prod_obj_add_cart.name} to your cart!', category='danger')
    return redirect(url_for('page_products'))
  
  if request.method == 'GET':
    product = Product.query.filter_by(owner=None)
    owner_products = Product.query.filter_by(owner=current_user.id)
    return render_template('products.html', product=product, buy_form=buy_form, owner_products=owner_products, sell_form=sell_form, add_cart_form=add_cart_form)

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

@app.route('/change_username', methods=['GET', 'POST', 'PUT'])
def page_change_username():
  form = ChangeUsernameForm()
  if form.validate_on_submit():
    user_exists = User.query.filter_by(username=form.username.data).first()
    if not user_exists:
      current_user.change_username(new_username=form.username.data)
      flash("Username changed!", category="success")
      return redirect(url_for('page_home'))
    else:
      flash("Error: username already exists!", category="danger")
  return render_template('change_username.html', form=form)

@app.route('/change_password', methods=['GET', 'POST', 'PUT'])
def page_change_password():
  form = ChangePasswordForm()
  if form.validate_on_submit():
    current_user.change_password(new_password=form.password1.data)
    flash("Password changed!", category="success")
    return redirect(url_for('page_home'))
  else:
    flash("Error: passwords do not match!", category="danger")
  return render_template('change_password.html', form=form)

@app.route('/delete_account', methods=['GET', 'POST', 'DELETE'])
def page_delete_account():
  current_user.delete_account()
  flash("Account deleted!", category="success")
  return redirect(url_for('page_home'))