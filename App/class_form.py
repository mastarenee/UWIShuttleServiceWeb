#Forms Handling and Management
from flask_wtf import Form 
from wtforms import TextField, IntegerField, TextAreaField, DateTimeField, SubmitField, RadioField, StringField, SelectField, PasswordField
from wtforms import validators, ValidationError

class RoutesForm(Form):

    name = TextField("Name Of Student",[validators.Required("Please enter your name.")])
    notes = TextAreaField("note")
    latitude = TextField("latitude",[validators.Required("Please enter your latitude.")])
    longitude = TextField("longitude",[validators.Required("Please enter your longitude.")])
    start = TextField('start',[validators.Required("Please enter a start time.")])
    end = TextField('end',[validators.Required("Please enter an end time.")])
    breaks = TextAreaField("breaks")
    submit = SubmitField("Send")

class AdminUserForm(Form):
    name = TextField("Name Of Admin User",[validators.Required("Please enter a full name.")])
    email = TextField("Email Address",[validators.Required("Please enter a valid email."), validators.Email("Please enter an email address.")] )
    telephone = TextField("Phone Number",[validators.Required("Please enter the phone number.")])
    
    password = PasswordField('New Password', [
        validators.EqualTo('confirmpassword', message='Passwords must match')
    ])
    confirmpassword = PasswordField("Confirm Password")

class AdminUpdateForm(Form):
    name = TextField("Name Of Admin User")
    email = TextField("Email Address")
    telephone = TextField("Phone Number")

    password = PasswordField('New Password')
    confirmpassword = PasswordField("Confirm Password")

class DriverForm(Form):
    name = TextField("Name Of Driver",[validators.Required("Please enter the name of the driver.")] )
    email = TextField("Email Address",[validators.Required("Please enter a valid email.")] )
    telephone = TextField("Phone Number", [validators.Required("Please enter a phone number.")])
    
    password = PasswordField('New Password', [
        validators.EqualTo('confirmpassword', message='Passwords must match')
    ])
    confirmpassword = PasswordField("Confirm Password")

class NewsForm(Form):
    name = TextField("Name Of Article",[validators.Required("Please enter an article title.")], render_kw={'readonly': True})
    description = TextAreaField("description",[validators.Required("Please enter a description.")], default="", render_kw={'readonly': True})
    expires = DateTimeField("expires", [validators.Required("Please enter an expiry date.")], render_kw={'readonly': True})

# To be Updated
class StudentForm(Form):
    name = TextField("Name Of Admin User",[validators.Required("Please enter the name.")])
    email = TextField("Email Address",[validators.Required("Please enter an email address."), validators.Email("Please enter an email address.")])
    telephone = TextField("Phone Number",[validators.Required("Please enter the phone number.")])
    password = PasswordField("Password")

    password = PasswordField('New Password', [
        validators.EqualTo('confirmpassword', message='Passwords must match')
    ])
    confirmpassword = PasswordField("Confirm Password")

# To be Updated
class ContactForm(Form):
    name = TextField("Name Of User",[validators.Required("Please enter the name.")])
    email = TextField("Email Address",[validators.Required("Please enter an email address."), validators.Email("Please enter an email address.")])
    subject = TextField("Subject",[validators.Required("Please enter a valid subject")])
    message = TextAreaField("Message",[validators.Required("Please enter the message.")])