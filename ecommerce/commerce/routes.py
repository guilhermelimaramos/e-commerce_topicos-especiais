from commerce import app
from flask import render_template, redirect, url_for, flash, request
from commerce.models import Product, User
from commerce.forms import SignUpForm, SignInForm, BuyProductForm, ChangeUsernameForm, ChangePasswordForm, AddCartForm, RemoveAllCartForm
from commerce import db
from flask_login import login_user, logout_user, login_required, current_user

@app.context_processor
def inject_products():
    buy_form = BuyProductForm()
    product = Product.query.all()
    owner_products = None
    subtotal = 0
    if current_user.is_authenticated:
        owner_products = Product.query.filter_by(owner=current_user.id)
        subtotal = (db.session.query(db.func.sum(Product.price)).filter(Product.owner == current_user.id, Product.status == 'cart').scalar())
        if subtotal is None:
          subtotal = 0
    return dict(product=product, owner_products=owner_products, subtotal=subtotal, buy_form=buy_form)

@app.route('/')
def page_home():
  remove_all_form = RemoveAllCartForm()
  return render_template('home.html', remove_all_form=remove_all_form)

@app.route('/products', methods=['GET', 'POST'])
@login_required
def page_products():
  buy_form = BuyProductForm()
  add_cart_form = AddCartForm()
  remove_all_form = RemoveAllCartForm()

  if request.method == 'POST':

    # Remove all product
    if 'remove_all' in request.form:
      all_cart_product = Product.query.filter_by(owner=current_user.id, status='cart').all()
      if all_cart_product:
        for product in all_cart_product:
          product.remove_all_cart()
        flash(f'You remove all products!', category='info')
      else:
        flash(f'Error: no products to remove!', category='danger')
      return redirect(url_for('page_products'))

    # Add to cart
    elif 'add_cart' in request.form:
      add_cart_product = request.form.get('add_cart')
      prod_obj_add_cart = Product.query.filter_by(name=add_cart_product).first()
      if prod_obj_add_cart:
        prod_obj_add_cart.add_cart(user=current_user)
        flash(f'Congratulations! product successfully added !', category='success')
      return redirect(url_for('page_products'))
  
  if request.method == 'GET':
    return render_template('products.html', buy_form=buy_form, remove_all_form=remove_all_form, add_cart_form=add_cart_form)

@app.route('/products/confirm_purchase', methods=['GET', 'POST'])
@login_required
def page_confirm_purchase():
  subtotal_str = (db.session.query(db.func.sum(Product.price)).filter(Product.owner == current_user.id, Product.status == 'cart').scalar())
  subtotal = int(subtotal_str) if subtotal_str else 0
  if User.purchase_available(user=current_user, subtotal=subtotal):
    Product.purchase(user=current_user, subtotal=subtotal)
    all_cart_product = Product.query.filter_by(owner=current_user.id, status='cart').all()
    for product in all_cart_product:
      product.complete_purchase()
    flash(f'Congratulations! You bought all product per R$ {subtotal}', category='success')
  else:
    flash(f'Error: insufficient balance to buy all products!', category='danger')
  return redirect(url_for('page_products'))

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