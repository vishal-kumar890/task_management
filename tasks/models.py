from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    task_name = models.CharField(max_length=200)
    task_description = models.TextField(blank=True)
    task_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')

    class Meta:
        indexes = [
            models.Index(fields=['task_status']),  # Index on task_status for filtering
            models.Index(fields=['assigned_to']),  # Index on assigned_to for fetching user tasks
        ]

    def __str__(self):
        return self.task_name


class RateLimitRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    endpoint = models.CharField(max_length=255)
    request_count = models.IntegerField(default=0)
    window_start = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'endpoint', 'window_start')

