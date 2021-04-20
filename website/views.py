from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Vehicle
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
        flash('DONE', category= 'success')

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


# @views.route('/vehicle', methods=['GET', 'POST'])
# def vehicle():
#     return render_template("vehicle.html", user=current_user)
