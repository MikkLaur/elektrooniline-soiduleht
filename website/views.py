from datetime import datetime

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Vehicle, Record
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():


    # if request.method == 'POST':
    #     mark = request.form.get('mark')
    #     model = request.form.get('model')
    #     year = request.form.get('year')
    #     regOdometer = request.form.get('regOdometer')
    #     avgFuelCons = request.form.get('avgFuelCons')
    #     vehicleTankCap = request.form.get('vehicleTankCap')
    #
    #     new_veh = Vehicle(mark=mark, model=model, year=year, reg_odometer=regOdometer,
    #                       avg_fuel_cons=avgFuelCons, vehicle_tank_cap=vehicleTankCap, user_id=current_user.id)
    #     db.session.add(new_veh)
    #     db.session.commit()
    #     flash('DONE', category='success')

    return render_template("index.html", user=current_user)



@views.route('/record/<vehicle_id>', methods=['GET', 'POST'])
@login_required
def record(vehicle_id):

    veh = Vehicle.query.filter_by(id=vehicle_id).first_or_404()
    # If vehicle has no records, this line will 404 the page.
    # e.g a newly registered vehicle will not have records
    #rec = Record.query.filter_by(vehicle_id=veh.user_id).first_or_404()


    if request.method == 'POST':
        refillDate = request.form.get('refillDate')
        refillSize = request.form.get('refillSize')
        odometer = request.form.get('odometer')
        fuelLeft = request.form.get('fuelLeft')
        avgSpeed = request.form.get('avgSpeed')
        strDateToDate = datetime.strptime(refillDate, '%Y-%m-%d').date()
        new_record = Record(vehicle_id=vehicle_id, refill_date=strDateToDate, refill_size=refillSize,
                            odometer=odometer, fuel_left=fuelLeft, avg_speed=avgSpeed)
        db.session.add(new_record)
        db.session.commit()

        flash('New record added to database', category='success')

    return render_template("record.html", user=current_user, vehicle=veh)


@views.route('/account')
@login_required
def account():

    return render_template("account.html", user=current_user)


@views.route('/mycars')
@login_required
def mycars():

    return render_template("my_cars.html", user=current_user)