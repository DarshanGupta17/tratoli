from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Task
from .serializers import TaskSerializer
import threading
from django.db.models import Count
from users.models import CustomUser
from .tasks import send_task_assignment_email
class TaskAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        task_id = request.query_params.get('task_id')
        if task_id:
            task = get_object_or_404(Task, pk=task_id, assigned_to=request.user)
            serializer = TaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        priority = request.query_params.get('priority')
        due_date = request.query_params.get('due_date')
        status_param = request.query_params.get('status')
        
        tasks = Task.objects.filter(assigned_to=request.user)
        
        if priority:
            tasks = tasks.filter(priority=priority)
        if due_date:
            tasks = tasks.filter(due_date=due_date)
        if status_param:
            tasks = tasks.filter(status=status_param)
        
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        user = request.user
        assigned_to = data.get("assigned_to")
        if assigned_to:
            assigned_user = get_object_or_404(CustomUser, email=assigned_to)
        data["assigned_to"] = assigned_user.pk
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            send_task_assignment_email.delay(serializer.get('id'))

            serializer.save(assigned_to=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        task_id = request.query_params.get('task_id')
        if not task_id:
            return Response({"error": "Task ID is required for updating a task."}, status=status.HTTP_400_BAD_REQUEST)
        task = get_object_or_404(Task, id=task_id, assigned_to=request.user)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        task = get_object_or_404(Task, pk=pk, assigned_to=request.user)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def generate_report():
    data = {
        "completed_tasks": Task.objects.filter(status="completed").count(),
        "pending_tasks": Task.objects.filter(status="pending").count(),
        "tasks_by_priority": Task.objects.values("priority").annotate(count=Count("priority")),
    }
    return data

@api_view(["GET"])
def report_view(request):
    report = {}

    def fetch_report():
        nonlocal report
        report = generate_report()

    thread = threading.Thread(target=fetch_report)
    thread.start()
    thread.join()

    return Response(report)
