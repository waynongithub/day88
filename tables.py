# from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
# import random
# from sqlalchemy.sql import functions
# from sqlalchemy import exists
# from flask import Flask, render_template, redirect, url_for
# from flask_bootstrap import Bootstrap5
# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField, SelectField, BooleanField, FloatField
# from wtforms.validators import DataRequired, URL
# from forms import CafeForm
# import csv

db = SQLAlchemy()
# db.init_app(app)


# Cafe TABLE Configuration
def get_column_titles():
    return ['Cafe Name', 'map_url', 'img_url', "Location", 'Seats', 'Has Toilet', 'Has Wifi',
            'Has Sockets', 'Can Take Calls', 'Coffee Price', ' ', ' ']


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def to_list(self):
        # titles = [self.column.name for column in self.__table__.columns]
        # print(f"titles={titles}")

        cafes = [getattr(self, column.name) for column in self.__table__.columns]
        # print(f"the cafes: {blue}{cafes}{nc}")

        # print(f"the cafes w titles:{yellow}{cafes_w_titles}{nc}")
        return cafes

