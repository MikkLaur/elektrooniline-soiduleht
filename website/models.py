from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    register_date = db.Column(db.DateTime(timezone=True), default=func.now())
    notes = db.relationship('Note')
    vehicles = db.relationship('Vehicle')


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reg_date = db.Column(db.DateTime(timezone=True), default=func.now())
    mark = db.Column(db.String(100))
    model = db.Column(db.String(100))
    year = db.Column(db.Integer)
    reg_odometer = db.Column(db.String(100))#reg od
    avg_fuel_cons = db.Column(db.Integer)
    vehicle_tank_cap = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))




