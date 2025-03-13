from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    assigned_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = ["id", "task_name", "task_description", "task_status", "created_at", "updated_at", 
                  "due_date", "assigned_to", "assigned_by"]
        read_only_fields = ["created_at", "updated_at"]

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['assigned_by'] = self.context['request'].user
        else:
            raise serializers.ValidationError({"assigned_by": "User must be authenticated."})
        return super().create(validated_data)
