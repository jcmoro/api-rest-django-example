"""
Capa de presentación: vistas REST que exponen la API.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer
from .services import TaskService
from .repositories import TaskRepository


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet que expone los endpoints CRUD de Task
    y un endpoint adicional: `complete`.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_permissions(self):
        """Permite lectura pública y escritura solo autenticada."""
        if self.action in ["list", "retrieve"]:
            return []
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """Usa el servicio para crear la tarea."""
        service = TaskService(repository=TaskRepository())
        task = service.create_task(
            owner=self.request.user, data=serializer.validated_data
        )
        serializer.instance = task

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def complete(self, request, pk=None):
        """Marca una tarea como completada (POST /api/tasks/{id}/complete/)."""
        service = TaskService(repository=TaskRepository())
        try:
            task = service.mark_complete(int(pk), request.user)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(TaskSerializer(task).data)
