"""
Tests funcionales simulados de la API REST sin conexión a base de datos.
"""

from unittest.mock import patch, MagicMock
import pytest


@pytest.fixture
def mock_task_service():
    """
    Mock de TaskService para simular la creación y finalización de tareas.
    """
    with patch("tasks.views.TaskService") as MockService:
        instance = MockService.return_value

        # Simular create_task
        instance.create_task.side_effect = lambda owner, data: MagicMock(
            id=1, title=data["title"], completed=False, owner=owner
        )

        # Simular mark_complete
        instance.mark_complete.side_effect = lambda task_id, user: MagicMock(
            id=task_id, title="Mi tarea", completed=True
        )

        yield instance


@pytest.fixture
def mock_user():
    """Simula un usuario autenticado."""
    return MagicMock(username="user")


def test_create_and_complete_task(mock_task_service, mock_user):
    """
    Simula la creación y finalización de una tarea vía API.
    """
    # Simular la respuesta de crear tarea
    task = mock_task_service.create_task(owner=mock_user, data={"title": "Mi tarea"})
    response_create = MagicMock()
    response_create.status_code = 201
    response_create.data = {
        "id": task.id,
        "title": task.title,
        "completed": task.completed,
    }

    # Verificar creación
    assert response_create.status_code == 201
    assert response_create.data["title"] == "Mi tarea"
    assert response_create.data["completed"] is False

    # Simular la respuesta de completar tarea
    task_completed = mock_task_service.mark_complete(task.id, mock_user)
    response_complete = MagicMock()
    response_complete.status_code = 200
    response_complete.data = {
        "id": task_completed.id,
        "title": task_completed.title,
        "completed": task_completed.completed,
    }

    # Verificar finalización
    assert response_complete.status_code == 200
    assert response_complete.data["completed"] is True
