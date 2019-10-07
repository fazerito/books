from books import db, login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    reviews = db.relationship("Review", backref="book", lazy=True)

    def __repr__(self):
        return f"Book({self.isbn}, {self.title}, {self.author}, {self.year})"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    reviews = db.relationship("Review", backref="author", lazy=True)

    def __repr__(self):
        return f"User({self.name}, {self.email})"


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    rating = db.Column(db.String, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User, lazy="joined", innerjoin=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
