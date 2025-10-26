# tasks/tests/test_services_mocked.py
from unittest.mock import patch, MagicMock
import pytest
from django.core.exceptions import ValidationError
from tasks.services import TaskService
from tasks.models import Task
from django.contrib.auth.models import User


# -------------------------------
# Test: create_task
# -------------------------------
def test_create_task_creates_object():
    mock_user = MagicMock(spec=User)
    service = TaskService()

    with patch.object(TaskService, "create_task") as mock_create:
        mock_task = MagicMock(spec=Task)
        mock_task.title = "Test"
        mock_create.return_value = mock_task

        task = service.create_task(owner=mock_user, data={"title": "Test"})
        mock_create.assert_called_once_with(owner=mock_user, data={"title": "Test"})
        assert task.title == "Test"


# -------------------------------
# Test: mark_complete_only_owner
# -------------------------------
def test_mark_complete_only_owner():
    mock_owner = MagicMock(spec=User)
    mock_other = MagicMock(spec=User)
    service = TaskService()

    mock_task = MagicMock(spec=Task)
    mock_task.id = 1
    mock_task.owner = mock_owner
    mock_task.completed = False

    # Patch mark_complete
    with patch.object(TaskService, "mark_complete") as mock_mark:
        # Caso correcto
        mock_mark.return_value = True
        assert service.mark_complete(mock_task.id, mock_owner) is True

        # Caso de otro usuario → lanza ValidationError
        mock_mark.side_effect = ValidationError("No eres el dueño")
        with pytest.raises(ValidationError):
            service.mark_complete(mock_task.id, mock_other)
