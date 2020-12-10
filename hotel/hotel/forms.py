from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, PasswordField, BooleanField,IntegerField,DateField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email,ValidationError

def length_check(form,field):
    if len(field.data) == 0:
        raise ValidationError('Fields should not be null')
    

class AddPostForm(FlaskForm):
    title = StringField('Title', validators=[ DataRequired()])
    description = TextAreaField('Description', validators = [DataRequired()])

class SignUpForm(FlaskForm):
    firstname= StringField('First Name', validators= [DataRequired(), length_check])
    lastname = StringField('Last Name', validators= [DataRequired()])
    username = StringField('User Name', validators= [ DataRequired(), Length(min=4)])
    password = PasswordField('Password',validators=[ DataRequired(), Length(min=6)])
    email = EmailField('Email', validators= [DataRequired(), Email()])
    submit = SubmitField('Sign Up')


class SignInForm(FlaskForm):
    email = EmailField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired(), Length(min=6, max=30)])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Sign In')

class AboutUserForm(FlaskForm):
    firstname= StringField('First Name', validators= [DataRequired(), length_check])
    lastname = StringField('Last Name', validators= [DataRequired()])
    username = StringField('User Name', validators= [ DataRequired(), Length(min=4)])
    password = PasswordField('Password',validators=[ DataRequired(), Length(min=6)])
    email = EmailField('Email', validators= [DataRequired(), Email()])

class RoomForm(FlaskForm):
    roomnumber = StringField('Room Number', validators=[DataRequired()])
    roomtype = StringField('Rooom type', validators=[DataRequired()])
    cost = IntegerField('Cost', validators=[DataRequired()])
    capacity = IntegerField('Capacity', validators=[DataRequired()])

class CheckAvailForm(FlaskForm):
    checkin_date = DateField('Check-in Date', format='%m/%d/%Y',validators=[DataRequired()])
    checkout_date = DateField('Check-out Date', format='%m/%d/%Y',validators=[DataRequired()])
    num_guests = IntegerField('Num Guests', validators=[DataRequired()])

class ReserveForm(FlaskForm):
    checkin_date = DateField('Check-in Date', format='%m/%d/%Y', validators=[DataRequired()])
    checkout_date = DateField('Check-out Date', format='%m/%d/%Y', validators=[DataRequired()])
    num_guests = IntegerField('Num Guests', validators=[DataRequired()])
    room_numbers = StringField('Rooms)', validators=[DataRequired()])
