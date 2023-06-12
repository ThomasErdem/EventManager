from flask import render_template
from flask_login import login_required, current_user
from .model_event import Event
from flask import Blueprint

bp_events = Blueprint('bp_events', __name__)


@bp_events.route('/event-list', methods=['GET'])
@login_required
def do_event_list():
    """
    Render the event list page.

    Returns:
        rendered_template: Rendered HTML template for the event list page.
    """
    events = Event.query.all()
    return render_template('event/event_list.html', events=events, user=current_user)
