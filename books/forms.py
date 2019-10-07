from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from books.models import User


class RegistrationForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email",
                        validators=[DataRequired(), Email()])
    password = PasswordField("Password",
                             validators=[DataRequired(), Length(min=3, max=20)])
    confirm_password = PasswordField("Confirm Password",
                                     validators=[DataRequired(), Length(min=3, max=20), EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(name=username.data).first()
        if user:
            raise ValidationError("That username is taken. Choose a different one.")

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("That email is taken. Choose a different one.")


class LoginForm(FlaskForm):
    username = StringField("Username",
                            validators=[DataRequired()])
    password = PasswordField("Password",
                            validators=[DataRequired(), Length(min=3, max=20)])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")


class SearchForm(FlaskForm):
    choices = [("ISBN", "ISBN"),
               ("Title", "Title"),
               ("Author", "Author")]
    select = SelectField("Search for a book: ", choices=choices)
    search = StringField("", validators=[DataRequired()])
    submit = SubmitField("Search")


class RateForm(FlaskForm):
    choices = [("1", "1"),
               ("2", "2"),
               ("3", "3"),
               ("4", "4"),
               ("5", "5")]
    radio = RadioField("Choose a rating: ", choices=choices)
    text = TextAreaField("Write something about it!", validators=[DataRequired()])
    submit = SubmitField("Rate")
