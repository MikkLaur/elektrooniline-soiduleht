from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    register_date = db.Column(db.DateTime(timezone=True), default=func.now())
    vehicles = db.relationship('Vehicle')

# Links User and Vehicle table together in a many-to-many relation
#  A vehicle may have multiple owners/users
class UsersToVehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))

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
    records = db.relationship('Record')


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime(timezone=True), default=func.now())
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    refill_date = db.Column(db.Date)
    odometer = db.Column(db.Integer)
    refill_size = db.Column(db.Integer)
    fuel_left = db.Column(db.Float)
    avg_speed = db.Column(db.Float)






