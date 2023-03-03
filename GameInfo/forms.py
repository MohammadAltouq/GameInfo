from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email

class UserSignupForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField()

class UserSigninForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Login')

class UserDataForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField()

class BasicSearch(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit_button = SubmitField('search')

class Details(FlaskForm):
    id = StringField('id', validators=[DataRequired()])
    submit_button = SubmitField('details')
    
class Profile_img(FlaskForm):
    file = FileField("Please select a file to upload.", validators=[DataRequired()])
    submit_button = SubmitField('submit')

class Fav(FlaskForm):
    data = StringField('data', validators=[DataRequired()])
    submit_button = SubmitField('Add To Favorites')
class Fav_delete(FlaskForm):
    id = StringField('id', validators=[DataRequired()])
    submit_button = SubmitField('Remove')

