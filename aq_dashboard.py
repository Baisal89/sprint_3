"""OpenAQ Air Quality Dahsboard with Flask"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import openaq




APP = Flask(__name__)
api = openaq.OpenAQ()
status, body = api.measurments(city='Los Angeles', parameter='pm25')
l = []
for i in range(len(body['results'])):
    l.append((body['results'] [i] ['data'] ['utc'], body['results'] [i] ['value']))

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
APP.config['SQLALCHEMY_ECHO'] = True


DB = SQLAlchemy()


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return 'Date: {} -- PM 2.5: {}'.format(self.datetime, self.value)

@APP.route('/')
def root():
    """Base view"""

    return str(list(Record.query.filter(Record.value >= 10).all()))

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Opne AQ and replace existing data"""
    DB.drop_all()
    DB.create_all()
    #TODO get data from OpenAQ, make Recors objects with it, and to db
    for x in range(len(body['results'])):
        datetime = str(body['results'][x]['date']['utc'])
        value = floar(body['results'][x]['value'])
        db_user = Record(datetime=datetime, value=value)
    DB.session.commit()
    return 'Data refreshed!'
