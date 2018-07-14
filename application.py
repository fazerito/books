import os
from models import *

from flask import Flask, session, render_template, flash, redirect, url_for
from forms import RegistrationForm, LoginForm
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "c805bb1ada0664c4ec07143114b523ce"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
Session(app)
db.init_app(app)

# Set up database


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
    if session["logged_in"] == True:
        flash("You have already logged in!", "danger")
        return redirect(url_for("index"))

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        email = user.email
        password = user.password
        if form.email.data == email and form.password.data == password:
            flash("You have been logged in!", "success")
            session["logged_in"] = True
            session["email"] = email
            return redirect(url_for("index"))
        else:
            flash("Login unsuccessful, please check your email and password.", "danger")
    return render_template("login.html", method=["POST"], form=form)

@app.route("/logout")
def logout():
    session["logged_in"] = False
    return render_template("/")

@app.route("/user/<string:username>")
def profile(username):
    name = request.form.get("name")
    email = request.form.get("email")
    return render_template("profile.html", name=name, email=email)

@app.route("/search", methods=["POST", "GET"])
def search():
    return render_template("search.html")

if __name__ == "__main__":
    app.run(debug=True)
