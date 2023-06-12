from flask import render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .model_meeting import Meeting
from event_app import db
import json
from datetime import datetime
from .views_meeting import bp_meetings



@bp_meetings.route('/add-meeting', methods=['GET', 'POST'])
@login_required
def do_meeting():
    if request.method == 'POST':
        meeting_id = request.form.get('meeting_id')
        meeting_subject = request.form.get('subject')
        meeting_description = request.form.get('description')
        meeting_location = request.form.get('location')
        date = request.form.get('date')
        meeting_time = request.form.get('time')
        if date:
            date = datetime.strptime(date, '%Y-%m-%d').date()
        else:
            date = None

        if meeting_id:
            meeting = Meeting.query.filter_by(id=meeting_id, user_id=current_user.id).first()
            if meeting:
                meeting.subject = meeting_subject
                meeting.description = meeting_description
                meeting.location = meeting_location
                meeting.date = date
                meeting.time = meeting_time
                db.session.commit()
                flash('Meeting updated!', category='success')
            else:
                flash('Meeting not found or you do not have permission to edit this meeting!', category='error')
        else:
            new_meeting = Meeting(subject=meeting_subject, description=meeting_description, location=meeting_location, user_id=current_user.id, date=date, time=meeting_time)
            db.session.add(new_meeting)
            db.session.commit()
            flash('Meeting added!', category='success')

    meetings = Meeting.query.filter_by(user_id=current_user.id).order_by(Meeting.date.desc()).all()
    return render_template("meeting/add_meeting.html", user=current_user, meetings=meetings)



@bp_meetings.route('/delete-meeting', methods=['POST'])
@login_required
def delete_meeting():
    meeting = json.loads(request.data)
    meetingId = meeting['meetingId']
    meeting = Meeting.query.get(meetingId)
    if meeting:
        if meeting.user_id == current_user.id:
            db.session.delete(meeting)
            db.session.commit()

    return jsonify({})

@bp_meetings.route('/update-meeting/<int:meeting_id>', methods=['GET', 'POST'])
@login_required
def update_meeting(meeting_id):
    # Retrieve the meeting from the database
    meeting = Meeting.query.get(meeting_id)

    if meeting:
        # Check if the user is the owner of the meeting
        if meeting.user_id == current_user.id:
            if request.method == 'POST':
                meeting.subject = request.form.get('subject')
                meeting.description = request.form.get('description')
                meeting.location = request.form.get('location')
                meeting.date = request.form.get('date')
                meeting.time = request.form.get('time')

                db.session.commit()
                flash('Meeting updated successfully', 'success')
                return redirect(url_for('views.do_meeting_list'))

            return render_template('meeting/update_meeting.html', meeting=meeting)
        else:
            flash('You do not have permission to edit this meeting', 'error')
    else:
        flash('Meeting not found', 'error')

    return redirect(url_for('views.do_meeting_list'))





def get_meetings():
    meetings = Meeting.query.all()
    meeting_list = []
    for meeting in meetings:
        meeting_dict = {
            'title': meeting.subject,
            'description': meeting.description,
            'location': meeting.location,
            'start': meeting.date.isoformat(),
            'time': meeting.time.isoformat(),
        }
        meeting_list.append(meeting_dict)
    return meeting_list