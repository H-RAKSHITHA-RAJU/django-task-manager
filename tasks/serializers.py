# tasks/serializers.py
from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        # Add 'user' to the list of fields to be included in the response
        fields = ['id', 'user', 'title', 'description', 'due_date', 'completed', 'created_at']  # <-- ADD 'user' HERE

        # Keep this line. It ensures that when creating/updating a task via the API,
        # the user cannot change the 'user' field manually. It will be set by the view.
        read_only_fields = ['user']