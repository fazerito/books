from flask import render_template, url_for, flash, redirect, request, session
from books import app, db, bcrypt
from books.forms import RegistrationForm, LoginForm
from flask_session import Session
from sqlalchemy.orm import scoped_session, sessionmaker
from books.models import *
from flask_login import login_user, current_user, logout_user, login_required

Session(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(name=form.username.data, password=hashed_pw, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash(f"Your account has been created, {form.username.data}! Log in now!", "success")
        return redirect(url_for("login"))
    return render_template("register.html", method=["POST"], form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(url_for("search")) if next_page else redirect(url_for("index"))
        else:
            flash("Login unsuccessful, please check your username and password.", "danger")
    return render_template("login.html", method=["POST"], form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/search", methods=["POST", "GET"])
@login_required
def search():
    if request.method == "POST":
        title = request.form.get("title")
        book = Book.query.filter_by(title=title).first()
        author = book.author
        year = book.year
        return render_template("book.html", title=title, author=author, year=year)
    else:
        return render_template("search.html")
