from wtforms import Form, StringField, SelectField, TextAreaField, validators, IntegerField, FileField, FloatField, \
    EmailField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, Email
from database.models import Contact_Us_Type


# contact_us_db = Contact_Us_Type.query.all()
# contact_us_type_list = []
# default_type = ('', 'Select')
# contact_us_type_list.append(default_type)
#
# for item in contact_us_db:
#     type_item = (item.type , item.type)
#     contact_us_type_list.append(type_item)
# def ContactUsType(contact_us_type_list):
#
#
#
#     default_type = ('', 'Select')
#     contact_us_type_list.append(default_type)
#     # for item in type_:
#     #     # type_item = (item.type , item.type)
#     #     # contact_us_type_list.append(type_item)
#     #     print(item.type)
#     print(contact_us_type_list)
#
#     return contact_us_type_list


class ContactUs(Form):
    name = StringField('Name:', [validators.Length(min=1, max=150), validators.DataRequired()] )
    email = EmailField('Email address', [validators.DataRequired(), Email(check_deliverability=False,
                                                                          message='Please Enter a Valid Email Address')])
    phone_number = StringField('Phone Number:', [validators.DataRequired()])
    # type = SelectField('Type of Enquiry', [validators.DataRequired()],choices=[('', 'Select'), ('General','General'), ('Product_Purchase','Product Purchase'), ('Order Issues','Order Related Issues'),('Report Vulnerability','Report Vulnerability')], default='')
    # type = SelectField('Type of Enquiry', [validators.DataRequired()],choices=contactUsList , default='')
    subject = StringField('Subject', [validators.DataRequired()])
    message = TextAreaField('Enter Your Message:', [validators.DataRequired()])

    def validate_phone_number(form, phone_number):
        if len(phone_number.data) != 8 or not phone_number.data.isdigit():
            raise ValidationError(message='Phone Number must be only 8 Digits')


def validate_type(form, field):
    type_ = field.data.title()
    unique = Contact_Us_Type.query.filter_by(type=type_).first()
    if field.data is None:
        raise ValidationError("Input is required")
    elif unique:
        raise ValidationError("Type Has already Been Added to Database! Please enter a Contact US type.")


class Enquiry_type(Form):
    enquiry_type_add = StringField('Contact Us Enquiry Type', validators=[validate_type])
