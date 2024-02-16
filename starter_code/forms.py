from datetime import datetime
from flask_wtf import FlaskForm 
from wtforms import (StringField, SelectField,
 SelectMultipleField, DateTimeField,
 BooleanField, TextAreaField)
from wtforms.validators import (DataRequired, Length, URL, ValidationError)
from enums import Genre, State

class ShowForm(FlaskForm):
    artist_id = StringField('artist_id')
    venue_id = StringField('venue_id')
    start_time = DateTimeField('start_time', validators=[DataRequired()], default=datetime.today())


class VenueForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(min=6, max=80)])
    city = StringField('city', validators=[DataRequired()])
    state = SelectField('state', validators=[DataRequired()], choices=State.choices())
    address = StringField('address', validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired(message='Invalid phone.')])
    image_link = StringField('image_link')
    genres = SelectMultipleField('genres', validators=[DataRequired()], choices=Genre.choices())
    facebook_link = StringField('facebook_link', validators=[URL()])
    website_link = StringField('website_link', validators=[URL()])
    seeking_talent = BooleanField('seeking_talent', default=False)
    seeking_description = TextAreaField('seeking_description')


class ArtistForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    state = SelectField('state', validators=[DataRequired()], choices=State.choices())
    phone = StringField('phone')
    image_link = StringField('image_link')
    genres = SelectMultipleField('genres', validators=[DataRequired()], choices=Genre.choices())
    facebook_link = StringField('facebook_link', validators=[URL()])
    website_link = StringField('website_link', validators=[URL()])
    seeking_venue = BooleanField('seeking_venue', default=False)
    seeking_description = TextAreaField('seeking_description')
