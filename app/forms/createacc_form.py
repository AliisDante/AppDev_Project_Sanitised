from wtforms import Form, StringField, SelectField, TextAreaField, validators, IntegerField, EmailField, PasswordField, ValidationError
from wtforms.fields import DateField, EmailField
from database.models import Employee, Customer

def integer(form, field):
    if len(str(field.data)) != len("helloooo"):
        raise ValidationError(message="Please enter 8 digits.")

class createemp(Form):
    name = StringField('Name:',[validators.Length(min=1,max=150),validators.DataRequired()],)
    gender = SelectField('Gender:', [validators.DataRequired()],choices=[('', 'Select'), ('M', 'Male'), ('F', 'Female')], default='')
    email= EmailField('Email:',[validators.Email(), validators.DataRequired()])
    password = PasswordField('Password:', [
        validators.Length(min=10),
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password:')
    contact = IntegerField('Contact Number:',[validators.DataRequired(), integer])
    position = SelectField('Select Position:',[validators.DataRequired()],choices=[('Select'), ('Full-time'), ('Part-time'), ('Intern'), ('Admin'), ('Others')], default='')


    def validate_email(self, email):
        unique = Employee.query.filter_by(email=email.data).first()
        unique2 = Customer.query.filter_by(email=email.data).first()
        if unique or unique2:
            raise ValidationError("Email already in database! Please enter a new email.")
    
class updateemp(Form):
    name = StringField('Name:',[validators.Length(min=1,max=150),validators.DataRequired()],)
    gender = SelectField('Gender:', [validators.DataRequired()],choices=[('', 'Select'), ('M', 'Male'), ('F', 'Female')], default='')
    contact = IntegerField('Contact Number:',[validators.DataRequired(), integer])
    password = PasswordField('Password:', [
        validators.Length(min=10),
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password:')
    position = SelectField('Select Position:',[validators.DataRequired()],choices=[('Select'), ('Full-time'), ('Part-time'), ('Intern'), ('Admin'), ('Others')], default='')


class createcust(Form):
    name = StringField('Name:',[validators.Length(min=1,max=150),validators.DataRequired()],)
    gender = SelectField('Gender:', [validators.DataRequired()],choices=[('', 'Select'), ('M', 'Male'), ('F', 'Female')], default='')
    email= EmailField('Email:',[validators.Email(), validators.DataRequired()])
    password = PasswordField('Password:', [
        validators.Length(min=10),
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password:')
    contact = IntegerField('Contact Number:',[validators.DataRequired(), integer])

    def validate_email(self, email):
        unique = Employee.query.filter_by(email=email.data).first()
        unique2 = Customer.query.filter_by(email=email.data).first()
        if unique or unique2:
            raise ValidationError("Email already in database! Please enter a new email.")

class updatecust(Form):
    name = StringField('Name:',[validators.Length(min=1,max=150),validators.DataRequired()],)
    gender = SelectField('Gender:', [validators.DataRequired()],choices=[('', 'Select'), ('M', 'Male'), ('F', 'Female')], default='')
    contact = IntegerField('Contact Number:',[validators.DataRequired(), integer])