import csv
import os
import pandas as pd
from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Task

@shared_task
def export_tasks_to_csv(user_email):
    file_path = os.path.join(settings.MEDIA_ROOT, 'tasks_export.csv')

    # Fetch tasks
    tasks = Task.objects.all().values('title', 'description', 'priority', 'status', 'due_date')

    # Write to CSV
    df = pd.DataFrame(list(tasks))
    df.to_csv(file_path, index=False)

    # Send email with file link
    email = EmailMessage(
        "Your Task Export is Ready",
        f"Download your file: {settings.MEDIA_URL}tasks_export.csv",
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
    )
    email.send()

    return "CSV Export Completed"
