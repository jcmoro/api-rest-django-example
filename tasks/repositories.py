"""
Capa de acceso a datos.
Encapsula la lógica de interacción con la base de datos (ORM).
"""

from .models import Task


class TaskRepository:
    """Repositorio responsable de las operaciones CRUD de Task."""

    def get(self, task_id):
        """Obtiene una tarea por su ID o None."""
        return Task.objects.filter(id=task_id).first()

    def create(self, **data):
        """Crea una nueva tarea en la base de datos."""
        return Task.objects.create(**data)

    def update(self, task, **data):
        """Actualiza los campos de una tarea existente."""
        for key, value in data.items():
            setattr(task, key, value)
        task.save()
        return task
