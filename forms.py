from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random
from sqlalchemy.sql import functions
from sqlalchemy import exists
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField, FloatField
from wtforms.validators import DataRequired, URL
import csv


class CafeForm(FlaskForm):
    name = StringField(label='Cafe name', validators=[DataRequired()])
    map_url = StringField(label='map_url', validators=[DataRequired(), URL()])
    img_url = StringField(label='img_url', validators=[DataRequired(), URL()])
    location = StringField(label="Location", validators=[DataRequired()])
    seats = StringField(label='Seats', validators=[DataRequired()])
    has_toilet = BooleanField(label='Has Toilet', default=False)
    has_wifi = BooleanField(label='Has Wifi', default=False)
    has_sockets = BooleanField(label='Has Sockets', default=False)
    can_take_calls = BooleanField(label='Can Take Calls', default=False)
    coffee_price = StringField(label='Coffee Price', validators=[DataRequired()])
    submit = SubmitField(label='Submit')

