from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DateTimeField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, URL, NumberRange, Length

class LectureCategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional()])
    submit = SubmitField('Save Category')

class LectureForm(FlaskForm):
    title = StringField('Lecture Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[Optional()])
    date = DateTimeField('Date and Time', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    duration = IntegerField('Duration (minutes)', validators=[Optional(), NumberRange(min=1)])
    location = StringField('Location', validators=[Optional(), Length(max=200)])
    speaker = StringField('Speaker', validators=[Optional(), Length(max=100)])
    youtube_link = StringField('YouTube Link', validators=[Optional(), URL()])
    materials_file = FileField('Materials (PDF)', validators=[
        Optional(),
        FileAllowed(['pdf'], 'PDFs only!')
    ])
    image = FileField('Image', validators=[
        Optional(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Save Lecture')