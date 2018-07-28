from flask import render_template, url_for, flash, redirect, request, session, jsonify
from books import app, db, bcrypt
from books.forms import RegistrationForm, LoginForm, SearchForm
from flask_session import Session
from sqlalchemy.orm import scoped_session, sessionmaker
from books.models import *
from flask_login import login_user, current_user, logout_user, login_required
import requests
import json

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
    form = SearchForm()
    books = []
    if request.method == "POST":
        choice = form.select.data
        search_string = form.search.data
        if choice == "ISBN":
            books = Book.query.filter(Book.isbn.like("%" + search_string + "%")).all()
        if choice == "Title":
            books = Book.query.filter(Book.title.like("%" + search_string + "%")).all()
        if choice == "Author":
            books = Book.query.filter(Book.author.like("%" + search_string + "%")).all()
        return render_template("results.html", books=books)
    return render_template("search.html", method=["POST"], form=form)

@app.route("/results")
def results(books):
    return render_template("results.html", books=books)

@app.route("/book/<string:title>")
@login_required
def book(title):
    book = Book.query.filter_by(title=title).first()
    title = book.title
    return render_template("book.html", title=title, book=book)

@app.route("/api/<string:isbn>")
def api(isbn):
    book = Book.query.filter_by(isbn=isbn).first()
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "vM2JXxPvhe3OfoiR9dvPg", "isbns": "1632168146"})
    data = res.json()
    return jsonify(
    title=book.title,
    author=book.author,
    year=book.year,
    isbn=book.isbn,
    review_count=data["books"][0]["work_ratings_count"],
    average_score=data["books"][0]["average_rating"]
    )
