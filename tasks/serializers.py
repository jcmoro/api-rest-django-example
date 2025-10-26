"""
Serializadores DRF que transforman objetos Task <-> JSON.
Incorporan validaciones específicas.
"""

from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """Serializa y valida objetos Task."""

    class Meta:
        model = Task
        fields = ["id", "title", "description", "completed", "owner", "created_at"]
        read_only_fields = ["id", "owner", "created_at"]

    def validate_title(self, value):
        """Valida longitud del título."""
        if len(value) > 200:
            raise serializers.ValidationError(
                "El título no puede superar los 200 caracteres."
            )
        return value
