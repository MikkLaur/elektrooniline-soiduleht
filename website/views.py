from datetime import datetime

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Vehicle, Record
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    if request.method == 'POST':
        mark = request.form.get('mark')
        model = request.form.get('model')
        year = request.form.get('year')
        regOdometer = request.form.get('regOdometer')
        avgFuelCons = request.form.get('avgFuelCons')
        vehicleTankCap = request.form.get('vehicleTankCap')

        new_veh = Vehicle(mark=mark, model=model, year=year, reg_odometer=regOdometer,
                          avg_fuel_cons=avgFuelCons, vehicle_tank_cap=vehicleTankCap, user_id=current_user.id)
        db.session.add(new_veh)
        db.session.commit()
        flash('DONE', category='success')

        #note = request.form.get('note')
        #
        # if len(note) < 1:
        #     flash('Note is too short!', category='error')
        # else:
        #     new_note = Note(data=note, user_id=current_user.id)
        #     db.session.add(new_note)
        #     db.session.commit()
        #     flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash('Note deleted!', category='success')

    return jsonify({})


@views.route('/record/<vehicle_id>', methods=['GET', 'POST'])
@login_required
def record(vehicle_id):



    print(current_user.id)
    veh = Vehicle.query.filter_by(id=vehicle_id).first_or_404()
    print(veh.user_id)
    if request.method == 'POST':
        refillDate = request.form.get('refillDate')
        print(refillDate)

        print("today: " + str(datetime.strptime(refillDate, '%Y-%m-%d').date()))

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
