"""
Data access layer.
Encapsulates the logic of interaction with the database (ORM).
"""

from .models import Task


class TaskRepository:
    """Repository responsible for Task CRUD operations."""

    def get(self, task_id):
        """Get a task by its ID or None."""
        return Task.objects.filter(id=task_id).first()

    def create(self, **data):
        """Create a new task in the database."""
        return Task.objects.create(**data)

    def update(self, task, **data):
        """Update fields of an existing task."""
        for key, value in data.items():
            setattr(task, key, value)
        task.save()
        return task
