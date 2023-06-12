from flask import render_template
from flask_login import login_required, current_user
from .model_task import Task
from flask import Blueprint
import matplotlib.pyplot as plt
import io
import base64
import numpy as np

bp_tasks = Blueprint('bp_tasks', __name__)

@bp_tasks.route('/task-list', methods=['GET'])
@login_required
def do_task_list():
    """
    Retrieves all tasks from the database and generates a task status distribution chart.

    Returns:
        rendered_template: Rendered HTML template for the task list page.
    """
    tasks = Task.query.all()

    # Generate the status counts
    status_counts = {}
    for task in tasks:
        status = task.status
        if status in status_counts:
            status_counts[status] += 1
        else:
            status_counts[status] = 1

    # Extract the status labels and counts
    labels = list(status_counts.keys())
    counts = [int(count) for count in status_counts.values()]

    # Clear the current figure
    plt.clf()

    # Generate the bar chart
    x = np.arange(len(labels))
    plt.bar(x, counts)
    plt.xlabel('Status')
    plt.ylabel('Count')
    plt.title('Task Status Distribution')
    plt.xticks(x, labels)
    plt.gca().get_xaxis().set_major_locator(plt.MaxNLocator(integer=True))  # Set x-axis ticks as integers only

    # Save the chart to a BytesIO object
    chart_image = io.BytesIO()
    plt.savefig(chart_image, format='png')
    chart_image.seek(0)

    # Encode the chart image to base64
    chart_base64 = base64.b64encode(chart_image.getvalue()).decode('utf-8')

    return render_template('task/task_list.html', tasks=tasks, user=current_user, chart_base64=chart_base64)
