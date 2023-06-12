from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class RegistrationForm(FlaskForm):
    username = StringField(label='Username', Validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=6, max=16)])
    confirm_password = PasswordField(label='Confirm Password', validators=[DataRequired(), Length(min=6, max=16)])
    submit = SubmitField(label='Sign Up', validators=[DataRequired()])


class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='login', validators=[DataRequired()])

class ResetRequestForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired()])
    submit = SubmitField(label='Reset Password', validators=[DataRequired()])

class ResetPasswordForm(FlaskForm):
    password = PasswordField(label='New Password', validators=[DataRequired(), Length(min=6, max=16)])
    confirm_password = PasswordField(label='Confirm New Password', validators=[DataRequired(), Length(min=6, max=16), EqualTo('password', message='Passwords must match')])
    submit = SubmitField(label='Reset Password', validators=[DataRequired()])