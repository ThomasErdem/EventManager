from flask import render_template
from flask_login import login_required
from ..bp_events.model_event import Event
from ..bp_meetings.model_meeting import Meeting
from ..bp_tasks.model_task import Task
from datetime import datetime
from flask import render_template
from flask_login import login_required
from datetime import datetime
from flask import Blueprint

bp_home = Blueprint('bp_home', __name__, cli_group=None)

@bp_home.route('/')
@login_required
def do_home():
    # get the current date and time
    current_datetime = datetime.now()

    # get the 3 upcoming events
    upcoming_events = Event.query.filter(Event.date >= current_datetime).order_by(Event.date.asc()).limit(3).all()

    # get the 3 upcoming meetings
    upcoming_meetings = Meeting.query.filter(Meeting.date >= current_datetime).order_by(Meeting.date.asc()).limit(3).all()

    # get the 3 upcoming tasks
    upcoming_tasks = Task.query.filter(Task.deadline >= current_datetime).order_by(Task.deadline.asc()).limit(3).all()

    #renders template home.html
    return render_template('general/home.html', upcoming_events=upcoming_events, upcoming_meetings=upcoming_meetings, upcoming_tasks=upcoming_tasks)