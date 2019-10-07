import csv
import os

from flask import Flask
from books.models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///books/site.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    f = open("books/book_list.csv")
    reader = csv.reader(f)
    header = next(reader)
    for isbn, title, author, year in reader:
        book = Book(isbn=isbn, title=title, author=author, year=year)
        db.session.add(book)
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        main()
