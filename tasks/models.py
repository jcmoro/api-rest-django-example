"""
Main domain model: Task
"""

from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    """Represents a task that belongs to a user."""

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
