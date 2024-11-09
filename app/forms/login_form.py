from wtforms import Form, StringField, SelectField, TextAreaField, validators, IntegerField, EmailField, PasswordField, BooleanField

class login(Form):
    email= EmailField('Email:',[validators.Email(), validators.DataRequired()])
    password = PasswordField('Password:',[validators.Length(min=10), validators.DataRequired()])
    remember = BooleanField('Remember me?')

class forget(Form):
    email= EmailField('Email:',[validators.Email(), validators.DataRequired()])

class reset(Form):
    password = PasswordField('New Password:', [
        validators.Length(min=10),
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password:')

class updatepw(Form):
    current = PasswordField('Current Password:',[validators.DataRequired(), validators.Length(min=10)])
    password = PasswordField('Password:', [
        validators.Length(min=10),
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password:')

