#!/usr/bin/env python
"""
Archivo principal de entrada para el proyecto Django.

Equivalente a `manage.py`, pero renombrado a `main.py`
para adaptarse al estándar del proyecto.
"""

import os
import sys

if __name__ == "__main__":
    # Define el módulo de configuración predeterminado de Django.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")

    # Ejecuta los comandos de administración (runserver, migrate, etc.)
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
