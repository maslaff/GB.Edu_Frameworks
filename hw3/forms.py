from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError


class Include(object):
    def __init__(self, digits=True, capital=True, message=None):
        self.digits = digits
        self.capital = capital
        if not message:
            message = f"Field must be include {'digits' if digits else ''} {'capital letters' if capital else ''}."
        self.message = message

    def __call__(self, form, field):
        d = field.data
        print(f"VALIDATORS DATA!!! --- {d}")
        if (self.digits and any(map(str.isdigit, d))) and (
            self.capital and any(map(str.isupper, d))
        ):
            print("VALIDATED!!!")
            return
        print("NOT VALIDATED!!!")
        raise ValidationError(self.message)


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


class RegistrationForm(FlaskForm):
    fname = StringField("First name", validators=[DataRequired()])
    lname = StringField("Last name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6),
            EqualTo(
                "confirm_password", message="Вайвай"
            ),  # ??? Сообщение не выводится!
            Include(),
        ],
    )
    confirm_password = PasswordField("Confirm password")
