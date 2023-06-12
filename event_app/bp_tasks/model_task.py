from event_app import db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.sql import func


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text, nullable=False)
    note = db.Column(db.Text, nullable=True)
    priority = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.date(datetime.now()))
    deadline = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(30))