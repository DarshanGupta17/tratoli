from users.models import CustomUser
from django.db import models
from django.utils import timezone

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Task(TimeStampModel):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    due_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return self.title
