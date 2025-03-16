from django.urls import path
from .views import TaskAPIView,report_view,export_tasks
urlpatterns = [
    path('', TaskAPIView.as_view(), name='task-list'),
    path('report/', report_view, name="task_report"),
    path('export/', export_tasks, name="task_export")
]
