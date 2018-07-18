from flask import render_template, url_for, flash, redirect, request, session
from books import app
from books.forms import RegistrationForm, LoginForm
from flask_session import Session
from sqlalchemy.orm import scoped_session, sessionmaker
from books.models import *
from books import db

Session(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", "success")
        user = User(name=form.username.data, password=form.password.data, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html", method=["POST"], form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if "username" in session:
        flash("You have already logged in!", "danger")
        return redirect(url_for("index"))

    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        username = user.name
        password = user.password
        if form.username.data == username and form.password.data == password:
            flash("You have been logged in!", "success")
            session["username"] = username
            return render_template("search.html")
        else:
            flash("Login unsuccessful, please check your email and password.", "danger")
            return redirect(url_for("login"))
    return render_template("login.html", method=["POST"], form=form)

@app.route("/logout")
def logout():
    if "username" in session:
        session.pop("username", None)
        flash("You have been successfully logged out!", "success")
        return render_template("index.html")
    else:
        flash("Log in first!", "danger")
        return redirect(url_for("login"))

@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        title = request.form.get("title")
        book = Book.query.filter_by(title=title).first()
        author = book.author
        year = book.year
    return render_template("book.html", title=title, author=author, year=year)

@app.route("/<string:title>")
def book(title):
    return
