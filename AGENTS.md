# UniCert V2

Sistema de certificación académica universitaria. API REST construida con FastAPI y PostgreSQL.

## Stack
- Lenguaje: Python 3.12
- Framework: FastAPI
- ORM: SQLAlchemy async
- Base de datos: PostgreSQL
- Tests: pytest (por implementar)

## Base de datos
- Actualmente: almacenamiento en memoria (stores)
- Objetivo V2: PostgreSQL con SQLAlchemy async + migraciones con Alembic
- Durante la migración no romper el comportamiento existente de los endpoints

## Comandos
- `uvicorn main:app --reload` — servidor local
- `pytest` — ejecutar tests
- `alembic upgrade head` — aplicar migraciones

## Estructura del proyecto
- `app/` — código principal
- `app/{modulo}/api/` — routers FastAPI
- `app/{modulo}/domain/` — entidades y schemas
- `app/{modulo}/repository/` — acceso a datos
- `app/{modulo}/services/` — lógica de negocio
- `app/core/` — utilidades compartidas

## Convenciones
- snake_case para variables y funciones
- Los routers solo construyen respuestas, no lógica
- Servicios retornan diccionarios limpios
- Respuestas estandarizadas con success_response() y error_response()
- Excepciones tipadas en cada módulo

## No hagas
- No mezclar lógica de negocio en los routers
- No acceder a la BD directamente desde servicios, usar repository
- No subir archivos .env al repositorio
- No instalar dependencias sin actualizar requirements.txt

## Flujo de trabajo
- Antes de cambios grandes propón un plan y espera aprobación
- Una tarea a la vez
- Los tests deben pasar antes de cada commit (cuando existan)
- Si no estás seguro al 80%, pregunta, no inventes