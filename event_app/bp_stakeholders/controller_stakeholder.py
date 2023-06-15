from event_app import db
import json
from flask import render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .model_stakeholder import Stakeholder
from .views_stakeholder import bp_stakeholders


@bp_stakeholders.route('/Stakeholders', methods=['GET', 'POST'])
@login_required
def do_stakeholder() -> str:
    """
    Handle stakeholder creation and update requests.
    Render the stakeholder page with a list of stakeholders.

    Returns:
        rendered_template: Rendered HTML template for the stakeholder page.
    """
    if request.method == 'POST':
        stakeholder_id = request.form.get('stakeholder_id')
        stakeholder_name = request.form.get('name')
        stakeholder_email = request.form.get('email')
        stakeholder_phone_number = request.form.get('phone number')
        stakeholder_type = request.form.get('type')
        stakeholder_company = request.form.get('company')

        if stakeholder_name is not None and len(stakeholder_name) < 1:
            flash('Event name is too short!', category='error')
        else:
            if stakeholder_id:
                stakeholder = Stakeholder.query.filter_by(id=stakeholder_id, user_id=current_user.id).first()
                if stakeholder:
                    stakeholder.name = stakeholder_name
                    stakeholder.email = stakeholder_email
                    stakeholder.phone_number = stakeholder_phone_number
                    stakeholder.type = stakeholder_type
                    stakeholder.company = stakeholder_company
                    db.session.commit()
                    flash('Stakeholder updated!', category='success')
                else:
                    flash('Stakeholder not found or you do not have permission to edit this stakeholder!', category='error')
            else:
                new_stakeholder = Stakeholder(name=stakeholder_name, email=stakeholder_email, phone_number=stakeholder_phone_number, type=stakeholder_type, company=stakeholder_company ,user_id=current_user.id)
                db.session.add(new_stakeholder)
                db.session.commit()
                flash('Stakeholder added!', category='success')

    stakeholders = Stakeholder.query.filter_by(user_id=current_user.id).order_by(Stakeholder.name.desc()).all()
    return render_template("stakeholder/add_stakeholder.html", user=current_user, stakeholders=stakeholders)


@bp_stakeholders.route('/delete-stakeholder', methods=['POST'])
@login_required
def delete_stakeholder() -> jsonify:
    """
    Handle stakeholder deletion request.

    Returns:
        json_response: Empty JSON response.
    """
    stakeholder = json.loads(request.data)
    stakeholderId = stakeholder['stakeholderId']
    stakeholder = Stakeholder.query.get(stakeholderId)
    if stakeholder:
        if stakeholder.user_id == current_user.id:
            db.session.delete(stakeholder)
            db.session.commit()

    return jsonify({})


@bp_stakeholders.route('/update-stakeholder/<int:stakeholder_id>', methods=['GET', 'POST'])
@login_required
def update_stakeholder(stakeholder_id) -> redirect:
    """
    Handle stakeholder update request.

    Args:
        stakeholder_id: ID of the stakeholder to be updated.

    Returns:
        response: Redirects to the stakeholder list page or renders the stakeholder update form.
    """
    # Retrieve the stakeholder from the database
    stakeholder = Stakeholder.query.get(stakeholder_id)

    if stakeholder:
        # Check if the user is the owner of the stakeholder
        if stakeholder.user_id == current_user.id:
            if request.method == 'POST':
                stakeholder.name = request.form.get('name')
                stakeholder.email = request.form.get('email')
                stakeholder.phone_number = request.form.get('phone_number')
                stakeholder.type = request.form.get('type')
                stakeholder.company = request.form.get('company')

                db.session.commit()
                flash('Stakeholder updated successfully', 'success')

                return redirect(url_for('bp_stakeholders.do_stakeholder_list'))

            return render_template('stakeholder/update_stakeholder.html', stakeholder=stakeholder)
        else:
            flash('You do not have permission to edit this stakeholder', 'error')
    else:
        flash('Stakeholder not found', 'error')

    return redirect(url_for('bp_stakeholders.do_stakeholder_list'))
