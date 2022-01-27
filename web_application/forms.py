from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.fields.simple import EmailField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Optional,
    ValidationError,
)


class RegistrationForm(FlaskForm):
    """Register form"""

    email = StringField("Email", validators=[Email(), DataRequired()])
    # first_name = StringField("First Name", validators=[DataRequired()])
    # last_name = StringField("Last Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[
                             DataRequired(), Length(min=6)])
    password_confirmation = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register", render_kw={
                         "class": "btn btn-primary w-100"})

    # # Will raise ValidationError if email is already in the database
    # def validate_email(self, email):
    #     user = User.query.filter_by(userEmail=email.data).first()
    #     if user:
    #         raise ValidationError("A user with this email already exists!")
