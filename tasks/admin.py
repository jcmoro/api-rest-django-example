"""
Django admin configuration for the Task model.
Adds actions that simulate common API operations:
- post: create a new sample task for the current user.
- put: full update of selected items (example: prefix the title).
- patch: partial update (toggle the "completed" state).
- delete: delete the selected tasks.

These actions are utilities to facilitate testing from the admin.
"""
from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _

from .models import Task
from .repositories import TaskRepository
from .services import TaskService


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "completed", "created_at")
    list_filter = ("completed", "owner")
    search_fields = ("title", "description", "owner__username")

    actions = (
        "action_post_task",
        "action_put_task",
        "action_patch_task",
        "action_delete_task",
    )

    repo = TaskRepository()
    service = TaskService(repo)

    def action_post_task(self, request, queryset):
        """
        Create a new sample task for the current user (request.user).
        It does not depend on the selected queryset, but a selection is required to enable the action.
        """
        data = {
            "title": _("Nueva tarea desde admin"),
            "description": _("Creada mediante acción POST en el admin"),
        }
        task = self.service.create_task(owner=request.user, data=data)
        messages.success(request, _(f"Tarea creada (ID {task.id})."))

    action_post_task.short_description = "POST: crear tarea de ejemplo"

    def action_put_task(self, request, queryset):
        """
        PUT: actualización "completa" de los objetos seleccionados.
        Como ejemplo, prefijamos el título con "[PUT] " manteniendo el resto.
        """
        updated = 0
        for task in queryset:
            new_title = f"[PUT] {task.title}"
            # Simulamos un PUT cambiando explícitamente el título
            self.repo.update(task, title=new_title)
            updated += 1
        if updated:
            messages.success(request, _(f"{updated} tarea(s) actualizada(s) con PUT."))
        else:
            messages.info(request, _("No hay tareas seleccionadas."))

    action_put_task.short_description = "PUT: prefijar título en seleccionadas"

    def action_patch_task(self, request, queryset):
        """
        PATCH: actualización parcial para alternar el campo 'completed'.
        """
        updated = 0
        for task in queryset:
            self.repo.update(task, completed=not task.completed)
            updated += 1
        if updated:
            messages.success(request, _(f"{updated} tarea(s) alternadas (completed)."))
        else:
            messages.info(request, _("No hay tareas seleccionadas."))

    action_patch_task.short_description = "PATCH: alternar 'completed' en seleccionadas"

    def action_delete_task(self, request, queryset):
        """
        DELETE: elimina las tareas seleccionadas.
        Se mantiene separada de la acción por defecto para hacerla explícita.
        """
        count = queryset.count()
        queryset.delete()
        messages.warning(request, _(f"{count} tarea(s) eliminadas."))

    action_delete_task.short_description = "DELETE: eliminar seleccionadas"
