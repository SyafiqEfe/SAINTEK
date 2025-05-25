from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Optional, URL, Length, Email

class MosqueInfoForm(FlaskForm):
    name = StringField('Mosque Name', validators=[DataRequired(), Length(max=200)])
    address = StringField('Address', validators=[DataRequired(), Length(max=255)])
    description = TextAreaField('Description', validators=[Optional()])
    history = TextAreaField('History', validators=[Optional()])
    vision = TextAreaField('Vision', validators=[Optional()])
    mission = TextAreaField('Mission', validators=[Optional()])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=100)])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    logo = FileField('Logo', validators=[
        Optional(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
    google_maps_link = StringField('Google Maps Link', validators=[Optional(), URL(), Length(max=255)])
    
    # Social media
    facebook = StringField('Facebook', validators=[Optional(), URL(), Length(max=255)])
    twitter = StringField('Twitter', validators=[Optional(), URL(), Length(max=255)])
    instagram = StringField('Instagram', validators=[Optional(), URL(), Length(max=255)])
    youtube = StringField('YouTube', validators=[Optional(), URL(), Length(max=255)])
    
    # Donation
    bank_account = StringField('Bank Account Number', validators=[Optional(), Length(max=100)])
    bank_name = StringField('Bank Name', validators=[Optional(), Length(max=100)])
    qris_image = FileField('QRIS Image', validators=[
        Optional(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
    
    submit = SubmitField('Update Information')

class QuoteForm(FlaskForm):
    quote_text = TextAreaField('Quote Text', validators=[DataRequired()])
    source = StringField('Source', validators=[Optional(), Length(max=200)])
    reference = StringField('Reference', validators=[Optional(), Length(max=200)])
    is_active = BooleanField('Is Active')
    submit = SubmitField('Save Quote')