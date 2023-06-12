from event_app import db
from datetime import date
from flask_login import UserMixin
from sqlalchemy.sql import func



class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(5000), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    budget = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    program = db.Column(db.String(50000), nullable=False)
    category = db.Column(db.String(30))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
