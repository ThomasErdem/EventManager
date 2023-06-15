from flask import render_template
from flask_login import login_required, current_user
from .model_task import Task
from flask import Blueprint
import matplotlib.pyplot as plt
from .utils import generateRandomColors
import io
import base64
import numpy as np

bp_tasks = Blueprint('bp_tasks', __name__)

@bp_tasks.route('/task-list', methods=['GET'])
@login_required
def do_task_list() -> str:
    """
    Retrieves all tasks from the database and generates a task status distribution chart.

    Returns:
        rendered_template: Rendered HTML template for the task list page.
    """
    tasks = Task.query.all()

    status_counts = {}
    for task in tasks:
        status = task.status
        if status in status_counts:
            status_counts[status] += 1
        else:
            status_counts[status] = 1

    total_tasks = len(tasks)
    status_percentages = {status: count / total_tasks * 100 for status, count in status_counts.items()}

    labels = list(status_percentages.keys())
    percentages = [round(percentage, 2) for percentage in status_percentages.values()]

    colors = generateRandomColors(len(labels))

    chart_image = io.BytesIO()
    plt.bar(labels, percentages, color=colors)
    plt.xlabel('Status')
    plt.ylabel('Percentage')
    plt.title('Task Status Distribution')
    plt.ylim(0, 100)
    plt.gca().get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0f}%'))
    plt.savefig(chart_image, format='png')
    chart_image.seek(0)

    chart_base64 = base64.b64encode(chart_image.getvalue()).decode('utf-8')

    return render_template('task/task_list.html', tasks=tasks, user=current_user, chart_base64=chart_base64)
