from event_app import db
import json
from datetime import datetime
from flask import render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .model_task import Task
from .views_task import bp_tasks

@bp_tasks.route('/add-task', methods=['GET', 'POST'])
@login_required
def do_task() -> str:
    """
    Handle task creation and update requests.
    Render the task page with a list of tasks.

    Returns:
        rendered_template: Rendered HTML template for the task page.
    """
    if request.method == 'POST':
        task_id = request.form.get('task_id')
        task_data = request.form.get('task')
        task_note = request.form.get('note')
        task_priority = request.form.get('priority')
        task_status = request.form.get('status')
        date = datetime.now().date()
        deadline = request.form.get('deadline')

        if deadline:
            deadline = datetime.strptime(deadline, '%Y-%m-%d').date()
        else:
            deadline = None

        if task_data is not None and len(task_data) < 1:
            flash('Task is too short!', category='error')
        else:
            if task_id:
                task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
                if task:
                    task.data = task_data
                    task.note = task_note or '-'  # set '-' as default if note is empty
                    task.priority = task_priority 
                    task.date = date
                    task.deadline = deadline
                    task.status = task_status
                    db.session.commit()
                    flash('Task updated!', category='success')
                else:
                    flash('Task not found or you do not have permission to edit this task!', category='error')
            else:
                new_task = Task(data=task_data, user_id=current_user.id, date=date, deadline=deadline, note=task_note or '-', priority=task_priority, status=task_status)
                db.session.add(new_task)
                db.session.commit()
                flash('Task added!', category='success')

    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.date.desc()).all()
    return render_template("task/add_task.html", user=current_user, tasks=tasks)


def get_tasks() -> list:
    """
    Get a list of all tasks.

    Returns:
        task_list: A list of task dictionaries.
    """
    tasks = Task.query.all()
    task_list = []
    for task in tasks:
        task_dict = {
            'title': task.data,
            'end': task.deadline.isoformat() if task.deadline is not None else None,
        }
        task_list.append(task_dict)
        print(task_dict)
    return task_list


@bp_tasks.route('/delete-task', methods=['POST'])
@login_required
def delete_task() -> jsonify:
    """
    Handle task deletion request.

    Returns:
        json_response: Empty JSON response.
    """
    task = json.loads(request.data)
    taskId = task['taskId']
    task = Task.query.get(taskId)
    if task:
        if task.user_id == current_user.id:
            db.session.delete(task)
            db.session.commit()

    return jsonify({})


@bp_tasks.route('/update-task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def update_task(task_id) -> redirect:
    """
    Handle task update request.

    Args:
        task_id: ID of the task to be updated.

    Returns:
        response: Redirects to the task list page or renders the task update form.
    """
    # Retrieve the task from the database
    task = Task.query.get(task_id)

    if task:
        # Check if the user is the owner of the task
        if task.user_id == current_user.id:
            if request.method == 'POST':
                task.data = request.form.get('data')
                task.note = request.form.get('note')
                task.priority = request.form.get('priority')
                task.deadline = request.form.get('deadline')
                task.status = request.form.get('status')

                db.session.commit()
                flash('Task updated successfully', 'success')
                return redirect(url_for('bp_tasks.do_task_list'))

            return render_template('task/update_task.html', task=task)
        else:
            flash('You do not have permission to edit this task', 'error')
    else:
        flash('Task not found', 'error')

    return redirect(url_for('bp_tasks.do_task_list'))
