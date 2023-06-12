from flask import render_template
from flask_login import login_required, current_user
from .model_stakeholder import Stakeholder
from flask import Blueprint

bp_stakeholders = Blueprint('bp_stakeholders', __name__)


@bp_stakeholders.route("/stakeholder-list", methods=['GET'])
@login_required
def do_stakeholder_list():
    stakeholders = Stakeholder.query.all()
    return render_template("stakeholder/stakeholder_list.html", stakeholders=stakeholders, user=current_user)