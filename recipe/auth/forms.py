from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from password_validator import PasswordValidator
from wtforms import ValidationError
import recipe.adapters.repository as repo
import recipe.auth.services as services

# Define password rules
password_schema = PasswordValidator()
password_schema \
    .min(8) \
    .max(20) \
    .has().uppercase() \
    .has().lowercase() \
    .has().digits() \
    .has().no().spaces()


class LoginForm(FlaskForm):
    """Form for user login"""
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    """Form for new user registration"""
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=25)]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=8, max=20)]
    )
    confirm = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match")
        ]
    )
    submit = SubmitField("Register")

    def validate_password(self, field):
        """Custom check to enforce strong password rules"""
        if not password_schema.validate(field.data):
            raise ValidationError(
                "Password must be 8–20 characters, include uppercase, lowercase, digits, and no spaces."
            )

    def validate_username(self, field):
        """Custom check to ensure username is unique"""
        existing_user = services.retrieve_user_by_name(field.data, repo.repo_instance)
        if existing_user is not None:
            raise ValidationError("Username already taken. Please choose another one.")
