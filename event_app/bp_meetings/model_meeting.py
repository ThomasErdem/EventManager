from event_app import db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.sql import func


class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), )