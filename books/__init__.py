
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "c805bb1ada0664c4ec07143114b523ce"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://dkhxrkcvbzxsjq:4c557995c15fa7c3e4f576cf7e743d64514099c3ddba7663d729c2a392e15925@ec2-54-247-79-32.eu-west-1.compute.amazonaws.com:5432/d1ason4t4rs4tf"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
#db.init_app(app)

from books import routes
