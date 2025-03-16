from django.urls import path
from .views import TaskAPIView,report_view
urlpatterns = [
    path('', TaskAPIView.as_view(), name='task-list'),
    path('report/', report_view, name="task_report"),
]
