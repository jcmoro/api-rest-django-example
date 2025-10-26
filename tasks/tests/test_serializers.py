# tasks/tests/test_serializers_mocked.py
from tasks.serializers import TaskSerializer


def test_title_validation():
    """Prueba la validación de longitud del título."""
    serializer = TaskSerializer(data={"title": "x" * 300})
    assert not serializer.is_valid()
    assert "title" in serializer.errors
