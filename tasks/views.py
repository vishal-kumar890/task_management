from django.utils import timezone
from django.conf import settings
from django.core.cache import cache
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task,RateLimitRecord
from .serializers import TaskSerializer
from .aws_integration import send_task_completed_notification
from django.db.models import Q
from rest_framework.exceptions import Throttled



# Mixin to add limiting on TaskViewSet
class RateLimitedViewMixin:

    def check_rate_limit(self, request, view_name):
        user = request.user
        cache_key = f"rate_limit:{user.id}:{view_name}"
        
        if not cache.add(cache_key, 1, timeout=settings.RATE_LIMIT_WINDOW):
            request_count = cache.get(cache_key, 0)
            if request_count >= settings.RATE_LIMIT_REQUESTS:
                return False
            cache.incr(cache_key, delta=1)

        # stored in the database as well
        if request.user.is_authenticated:
            rate_record, created = RateLimitRecord.objects.get_or_create(
                user=user,
                endpoint=view_name,
                window_start__date=timezone.now().date(),
                defaults={'request_count': 1}
            )

            if not created:
                rate_record.request_count += 1
                rate_record.save()

        return True

    def initial(self, request, *args, **kwargs):
        # This will enforce the rate limit on requests before processing
        view_name = self.__class__.__name__

        if not self.check_rate_limit(request, view_name):
            raise Throttled(detail="Rate Limit Exceeded. Please Try Again Later.")

        return super().initial(request, *args, **kwargs)


class TaskViewSet(RateLimitedViewMixin, viewsets.ModelViewSet):
    # This ViewSet handle CRUD operations for the Task model.

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['task_status', 'assigned_to']
    ordering_fields = ['created_at', 'updated_at', 'due_date']
    search_fields = ['task_name', 'task_description']

    def get_queryset(self):
        # Fetch tasks created or assigned to current user
        user = self.request.user
        return Task.objects.filter(Q(assigned_to=user) | Q(assigned_by=user))

    def perform_update(self, serializer):
        # This will handle the task status and trigger AWS notification if task completed
        instance = serializer.instance
        previous_status = instance.task_status.lower()
        updated_instance = serializer.save()
        new_status = updated_instance.task_status.lower()

        if previous_status != "completed" and new_status == "completed":
            send_task_completed_notification(updated_instance)

        return updated_instance

    @action(detail=False, methods=['get'])
    def my_tasks(self, request):
        # Custom endpoint to fetch tasks
        tasks = self.get_queryset()
        page = self.paginate_queryset(tasks)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
