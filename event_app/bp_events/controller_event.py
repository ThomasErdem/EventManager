from flask import render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .model_event import Event
from event_app import db
import json
from datetime import datetime
from .views_event import bp_events

@bp_events.route('/add-events', methods=['GET', 'POST'])
@login_required
def do_event() -> str:
    """
    renders the add_event template
    add new events to the app
    """
    if request.method == 'POST':
        event_id = request.form.get('event_id')
        event_name = request.form.get('name')
        event_description = request.form.get('description')
        event_location = request.form.get('location')
        date = request.form.get('date')
        event_budget = request.form.get('budget')
        event_program = request.form.get('program')
        event_category = request.form.get('category')
        if date:
            date = datetime.strptime(date, '%Y-%m-%d').date()
        else:
            date = None

        if event_name is not None and len(event_name) < 1:
            flash('Event name is too short!', category='error')
        if event_description is not None and len(event_description) < 1:
            flash('You have to fill in a description', category='error')
        if event_location is not None and len(event_location) < 1:
            flash('You have to fill in a location!', category='error')
        if event_budget is None or (event_budget is not None and len(event_budget) <1):
            flash('You have to set a budget!', category='error')
        if event_program is not None and len(event_program) < 1:
            flash('You have to fill in a program', category='error')
        if event_category is not None and len(event_category) < 1:
            flash('you have to set the category', category='error')
        else:
            if event_id:
                event = Event.query.filter_by(id=event_id, user_id=current_user.id).first()
                if event:
                    event.name = event_name
                    event.description = event_description
                    event.location = event_location
                    event.budget = event_budget
                    event.date = date
                    event.program = event_program
                    event.category = event_category
                    db.session.commit()
                    flash('Event updated!', category='success')
                else:
                    flash('Event not found or you do not have permission to edit this event!', category='error')
            else:
                new_event = Event(name=event_name, description=event_description, location=event_location, budget=event_budget, user_id=current_user.id, date=date, program=event_program, category=event_category)
                db.session.add(new_event)
                db.session.commit()
                flash('Event added!', category='success')

    events = Event.query.filter_by(user_id=current_user.id).order_by(Event.date.desc()).all()
    return render_template("event/add_event.html", user=current_user, events=events)

def get_events() -> list:
    """
    retrieve all events from database
    """
    events = Event.query.all()
    event_list = []
    for event in events:
        event_dict = {
            'title': event.name,
            'description': event.description,
            'location': event.location,
            'budget': event.budget,
            'start': event.date.isoformat(),
            'category': event.category
        }
        event_list.append(event_dict)
    return event_list



@bp_events.route('/delete-event', methods=['GET', 'POST'])
@login_required
def delete_event() -> jsonify:
    """
    deletes events from database
    """
    event = json.loads(request.data)
    eventId = event['eventId']
    event = Event.query.get(eventId)
    if event:
        if event.user_id == current_user.id:
            db.session.delete(event)
            db.session.commit()

    return jsonify({})

@bp_events.route('/update-event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def update_event(event_id) -> redirect:
    # Retrieve the meeting from the database
    event = Event.query.get(event_id)

    if event:
        # Check if the user is the owner of the meeting
        if event.user_id == current_user.id:
            if request.method == 'POST':
                event.name = request.form.get('name')
                event.description = request.form.get('description')
                event.location = request.form.get('location')
                event.budget = request.form.get('budget')
                event.date = request.form.get('date')
                event.program = request.form.get('program')
                event.category = request.form.get('category')

                db.session.commit()
                flash('Event updated successfully', 'success')
                return redirect(url_for('bp_events.do_event_list'))

            return render_template('event/update_event.html', event=event)
        else:
            flash('You do not have permission to edit this event', 'error')
    else:
        flash('Event not found', 'error')

    return redirect(url_for('bp_events.do_event_list'))