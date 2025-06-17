from datetime import date, datetime
from extensions import db

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    contacts = db.Column(db.String(200), nullable=False)
    goal = db.Column(db.String(200), nullable=True)
    subscriptions = db.relationship('Subscription', backref='client', lazy=True)

class Trainer(db.Model):
    __tablename__ = 'trainers'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    schedule = db.Column(db.Text, nullable=True)

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    valid_until = db.Column(db.Date, nullable=False)

    def is_active(self):
        return date.today() <= self.valid_until