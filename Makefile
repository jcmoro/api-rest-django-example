# ============================================================
# Makefile para automatizar tareas comunes del proyecto Django
# ============================================================

# -------------------------------------------------------------------
# Variables
# -------------------------------------------------------------------
COMPOSE = docker compose
WEB     = web
DB      = db

# -------------------------------------------------------------------
##@ 📖 Help automático
# -------------------------------------------------------------------
.PHONY: help create-admin
help: ## Display help
	@awk 'BEGIN {FS = ":.*##"; printf "${COLOR_HELP}${PROJECT_NAME}${COLOR_RESET}\n${PROJECT_DESCRIPTION}\n\nUsage:\n make ${COLOR_HELP}<target>${COLOR_RESET}\n"} /^[a-zA-Z_-]+:.*?##/ { printf " ${COLOR_HELP}%-30s${COLOR_RESET} %s\n", $$1, $$2 } /^##@/ { printf "\n${COLOR_BOLD}%s${COLOR_RESET}\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

create-admin: ## Create user admin django
	@read -p "Username (default: admin): " USER; \
	USER=$${USER:-admin}; \
	read -p "Email (default: admin@example.com): " EMAIL; \
	EMAIL=$${EMAIL:-admin@example.com}; \
	read -s -p "Password: " PASS; echo; \
	if [ -z "$$PASS" ]; then echo "Password vacía, abortando"; exit 1; fi; \
	docker compose run --rm \
		-e DJANGO_SUPERUSER_USERNAME=$$USER \
		-e DJANGO_SUPERUSER_EMAIL=$$EMAIL \
		-e DJANGO_SUPERUSER_PASSWORD=$$PASS \
		web python main.py createsuperuser --noinput

# -------------------------------------------------------------------
##@ 🐳 Docker
# -------------------------------------------------------------------
.PHONY: build up run down restart logs

build: ## Construye las imágenes Docker (sin caché)
	$(COMPOSE) build --no-cache

up: build makemigrations migrate ## Levanta los contenedores (construye primero)
	$(COMPOSE) up -d

run: ## Levanta el servidor de desarrollo
	docker compose run --rm web python main.py runserver 0.0.0.0:8000

down: ## Detiene y elimina contenedores, redes y volúmenes
	$(COMPOSE) down -v --remove-orphans

restart: ## Reinicia completamente el entorno
	$(COMPOSE) down --volumes
	$(COMPOSE) up -d

logs: ## Muestra los logs del servicio web
	$(COMPOSE) logs -f $(WEB)

# -------------------------------------------------------------------
##@ ⚙️ Django
# -------------------------------------------------------------------
.PHONY: migrate makemigrations shell

migrate: ## Ejecuta migraciones de Django
	$(COMPOSE) run --rm $(WEB) python main.py migrate

makemigrations: ## Crea nuevas migraciones
	$(COMPOSE) run --rm $(WEB) python main.py makemigrations tasks

shell: ## Abre una shell interactiva de Django
	$(COMPOSE) run --rm $(WEB) python main.py shell

# -------------------------------------------------------------------
##@ 🧪 Tests
# -------------------------------------------------------------------
.PHONY: test test-unit test-functional list-tasks

test: test-unit test-functional ## Ejecuta todos los tests (unitarios + funcionales)

test-unit: ## Ejecuta solo tests unitarios mockeados (rápidos, sin DB)
	docker compose run --rm web pytest -q tasks/tests/test_services.py tasks/tests/test_serializers.py

test-functional: ## Ejecuta tests funcionales (requieren DB)
	docker compose up -d db
	docker compose run --rm web pytest -q tasks/tests/test_api.py
	docker compose down

list-tasks: ## Ejecuta lista de tareas en local
	curl -s -H "Accept: application/json" http://localhost:8000/api/tasks/

# -------------------------------------------------------------------
##@ 🔍 Calidad de código
# -------------------------------------------------------------------
.PHONY: lint format

lint: ## Ejecuta flake8 para revisar el estilo de código
	$(COMPOSE) run --rm $(WEB) flake8 .

format: ## Ejecuta black para formatear el código automáticamente
	$(COMPOSE) run --rm $(WEB) black .
