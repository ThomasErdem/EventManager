from flask import render_template
from flask_login import login_required, current_user
from ..bp_events.controller_event import get_events
from ..bp_meetings.controller_meeting import get_meetings
from ..bp_tasks.controller_task import get_tasks
from flask import Blueprint

bp_calendar = Blueprint('bp_calendar', __name__)

@bp_calendar.route('/calendar', methods=['GET'])
@login_required
def do_calendar() -> str:
    """
    Render the calendar page.

    Returns:
        rendered_template: Rendered HTML template for the calendar page.
    """
    events = get_events()
    meetings = get_meetings()
    tasks = get_tasks()
    return render_template('calendar/calendar.html', events=events, meetings=meetings, tasks=tasks)
