from wtforms import Form, StringField, SelectField, TextAreaField, validators, IntegerField , FileField , FloatField

class PostForm(Form):
    title = StringField("Title",  [validators.DataRequired()])
    content = TextAreaField('Review Content', [validators.DataRequired()])
    rating = IntegerField('Rating', [validators.DataRequired()])