from event_app import db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.sql import func


class Stakeholder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(150))
    phone_number = db.Column(db.Integer)
    type = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    company = db.Column(db.String(45))