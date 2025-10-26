"""
Capa de dominio: lógica de negocio.
Define las operaciones principales sobre las tareas.
"""

from django.core.exceptions import ValidationError
from .repositories import TaskRepository


class TaskService:
    """Servicio que contiene las reglas de negocio del modelo Task."""

    def __init__(self, repository: TaskRepository = None):
        self.repo = repository or TaskRepository()

    def create_task(self, owner, data: dict):
        """Crea una nueva tarea, validando datos antes de persistir."""
        if data.get("title") and len(data["title"]) > 200:
            raise ValidationError("El título es demasiado largo.")
        data["owner"] = owner
        return self.repo.create(**data)

    def mark_complete(self, task_id: int, user):
        """Marca una tarea como completada si pertenece al usuario."""
        task = self.repo.get(task_id)
        if not task:
            raise ValidationError("Tarea no encontrada.")
        if task.owner != user:
            raise ValidationError("No tienes permiso para modificar esta tarea.")
        return self.repo.update(task, completed=True)
