from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL, Email, Length
from flask_ckeditor import CKEditorField

##WTForm


class AddCafe(FlaskForm):
    cafe_name = StringField("Cafe Name", validators=[DataRequired()])
    address = StringField("Location", validators=[DataRequired()])
    wifi = SelectField('Wifi',choices=['🚫','📶','📶 📶','📶 📶 📶'], validators=[DataRequired()])
    seating = SelectField('Seating', choices=['🚫','🪑','🪑 🪑','🪑 🪑 🪑'], validators=[DataRequired()])
    food = SelectField('Food & Coffee', choices=['🚫','🍽','🍽 🍽','🍽 🍽 🍽'], validators=[DataRequired()])
    cost = SelectField('Cost', choices=['🚫','💲', '💲 💲', '💲 💲 💲'], validators=[DataRequired()])
    description = StringField("Short Description", validators=[DataRequired()])
    submit = SubmitField("Add Cafe")

class EditCafe(FlaskForm):
    cafe_name = StringField("Cafe Name", validators=[DataRequired()])
    address = StringField("Location", validators=[DataRequired()])
    wifi = SelectField('WiFi',choices=['🚫','📶','📶 📶','📶 📶 📶'], validators=[DataRequired()])
    seating = SelectField('Seating', choices=['🚫','🪑','🪑 🪑','🪑 🪑 🪑'], validators=[DataRequired()])
    food = SelectField('Food & Coffee', choices=['🚫','🍽','🍽 🍽','🍽 🍽 🍽'], validators=[DataRequired()])
    cost = SelectField('Cost', choices=['🚫','💲', '💲 💲', '💲 💲 💲'], validators=[DataRequired()])
    description = StringField("Short Description", validators=[DataRequired()])
    submit = SubmitField("Update")


class AddWebsiteComments(FlaskForm):
    comment = CKEditorField("Comment", validators=[DataRequired()])
    commentator_name = StringField("Your Display Name", validators=[DataRequired()])
    commentator_email = StringField("Email",validators=[DataRequired(),Email()])
    submit = SubmitField("Add Comment")

class CafeReviews(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    author_email = StringField("Email",validators=[DataRequired(),Email()])
    review = CKEditorField("Description", validators=[DataRequired()])
    submit = SubmitField("Add Review")
