from celery import shared_task
from django.core.mail import send_mail
from .models import Task
from datetime import timedelta
from django.utils.timezone import now
from TMS.settings import EMAIL_HOST_USER  # Import settings properly

@shared_task
def send_task_assignment_email(task_id):
    try:
        task = Task.objects.get(id=task_id)
        if task.assigned_to and task.assigned_to.email:
            send_mail(
                'New Task Assigned',
                f'You have been assigned a new task: {task.title}.',
                EMAIL_HOST_USER,
                [task.assigned_to.email],
                fail_silently=False,
            )
    except Task.DoesNotExist:
        pass  # Handle the case where the task doesn't exist

@shared_task
def send_due_date_reminder():
    tasks = Task.objects.filter(due_date__lte=now() + timedelta(days=1), status="Pending")
    print(tasks)
    for task in tasks:
        if task.assigned_to and task.assigned_to.email:
            send_mail(
                'Task Due Soon',
                f'Task "{task.title}" is due within 24 hours.',
                EMAIL_HOST_USER,  # Use the configured sender email
                [task.assigned_to.email],
                fail_silently=False,
            )
