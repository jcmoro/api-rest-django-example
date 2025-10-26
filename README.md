# 🧩 Django REST API — Clean Architecture + SOLID + Docker

Este proyecto es un **ejemplo práctico y educativo** de cómo construir una **API REST profesional** con:
- **Django 4.2 + Django REST Framework**
- **Principios SOLID y Clean Code**
- **Docker y docker-compose**
- **Makefile** para automatizar tareas
- **Tests unitarios y funcionales** con Pytest

---

## 🚀 Objetivo

Demostrar cómo estructurar un proyecto Django de forma modular, mantenible y fácilmente testeable, separando responsabilidades en capas.

| Capa | Carpeta | Responsabilidad |
|------|----------|-----------------|
| **API / Infraestructura** | `api/` | Configuración general de Django y URLs globales |
| **Dominio / Aplicación** | `tasks/` | Modelos, lógica de negocio, serialización, servicios y endpoints |
| **Infraestructura externa** | `Dockerfile`, `docker-compose.yml` | Contenedores y dependencias |
| **Automatización / DevOps** | `Makefile` | Comandos para ejecutar tareas comunes |

---

## Frontend: 
    http://0.0.0.0:8000/api/tasks/

## Admin: 
    http://0.0.0.0:8000/admin/tasks/task/

## 📂 Estructura del proyecto

```
todo_api_example/
├── Makefile
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── requirements.txt
├── pytest.ini
├── main.py
├── api/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── tasks/
    ├── __init__.py
    ├── apps.py
    ├── models.py
    ├── serializers.py
    ├── repositories.py
    ├── services.py
    ├── views.py
    ├── urls.py
    └── tests/
        ├── test_serializers.py
        ├── test_services.py
        └── test_api.py
```

---

## ⚙️ Instalación y ejecución

### 1️⃣ Clonar el proyecto
```bash
git clone https://github.com/tuusuario/todo_api_example.git
cd todo_api_example
```

### 2️⃣ Construir e iniciar los contenedores
```bash
make up
```

### 3️⃣ Aplicar migraciones
```bash
make migrate
```

### 4️⃣ Abrir la API
La API estará disponible en 👉 [http://localhost:8000/api/tasks/](http://localhost:8000/api/tasks/)

---

## 🧪 Tests

Ejecuta **todos los tests** (unitarios + funcionales):
```bash
make test
```

Ejecuta solo los **unitarios**:
```bash
make test-unit
```

Ejecuta solo los **funcionales**:
```bash
make test-functional
```

---

## 🧠 Principios aplicados

- **Single Responsibility Principle (SRP)**: cada clase cumple un propósito específico.
- **Open/Closed Principle (OCP)**: los servicios y repositorios pueden extenderse sin modificar el código existente.
- **Dependency Inversion Principle (DIP)**: los `services` dependen de abstracciones (`repositories`), no de implementaciones concretas.
- **Clean Code**: código legible, funciones cortas, nombres descriptivos y separación lógica.

---

## 📡 Endpoints

| Método | Ruta | Descripción |
|---------|------|-------------|
| `GET` | `/api/tasks/` | Lista de tareas |
| `POST` | `/api/tasks/` | Crea una nueva tarea |
| `POST` | `/api/tasks/{id}/complete/` | Marca la tarea como completada |
| `GET` | `/api/tasks/{id}/` | Detalle de una tarea |
| `PUT/PATCH/DELETE` | `/api/tasks/{id}/` | Operaciones CRUD |

```
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept
[
    {
        "id": 1,
        "title": "Tarea prueba 1",
        "description": "Tarea prueba 1 description",
        "completed": false,
        "owner": 1,
        "created_at": "2025-10-26T18:31:31.452551Z"
    }
]
```

## 🧰 Comandos Makefile disponibles

Para ver todas las opciones disponibles en el `Makefile`, ejecuta:

```bash
make help
```

### Ejemplo de implementación en el Makefile

```makefile
Usage:
 make <target>

📖 Help automático
 help                  Display help
 create-admin          Create user admin django

🐳 Docker
 build                 Construye las imágenes Docker (sin caché)
 up                    Levanta los contenedores (construye primero)
 run                   Levanta el servidor de desarrollo
 down                  Detiene y elimina contenedores, redes y volúmenes
 restart               Reinicia completamente el entorno
 logs                  Muestra los logs del servicio web

⚙️ Django
 migrate               Ejecuta migraciones de Django
 makemigrations        Crea nuevas migraciones
 shell                 Abre una shell interactiva de Django

🧪 Tests
 test                  Ejecuta todos los tests (unitarios + funcionales)
 test-unit             Ejecuta solo tests unitarios mockeados (rápidos, sin DB)
 test-functional       Ejecuta tests funcionales (requieren DB)
 list-tasks            Ejecuta lista de tareas en local

🔍 Calidad de código
 lint                  Ejecuta flake8 para revisar el estilo de código
 format                Ejecuta black para formatear el código automáticamente
 
```

---

## 🧑‍💻 Autor
**José Carlos Moro Díaz**  
💼 GitHub: [@jcmoro](https://github.com/jcmoro)  
✉️ Contacto: jcmorodiaz@gmail.com