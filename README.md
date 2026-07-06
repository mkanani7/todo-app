# To-Do App API

A Django REST Framework backend for a simple to-do application with JWT authentication, user management, and todo CRUD operations.

## Features

- Register users
- Login with JWT authentication
- Create, read, update, and delete todos
- Mark todos as done or undone
- Set a reminder time for each todo
- Explore the API with Swagger UI

## Tech Stack

- Python 3.12+
- Django 6+
- Django REST Framework
- Simple JWT for authentication
- drf-spectacular for API documentation

## Project Structure

- accounts: user authentication and user-related APIs
- todos: todo model, serializers, views, and routes
- to_do_server: Django project configuration

## Installation

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies

```bash
cd ./to-do-app
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Run the Server

```bash
cd ./to-do-app/to_do_server
python manage.py migrate
python manage.py runserver
```

The API will be available at:

- http://127.0.0.1:8000/api/users/
- http://127.0.0.1:8000/api/todos/
- http://127.0.0.1:8000/api/token/
- http://127.0.0.1:8000/api/docs/

## Authentication

This project uses JWT authentication.

### Obtain a token

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'
```

### Use the token

```bash
curl -X GET http://127.0.0.1:8000/api/todos/ \
  -H "Authorization: Bearer <access_token>"
```

## API Endpoints

### Users
- POST /api/users/ - create a user
- POST /api/users/login/ - login helper endpoint
- GET /api/users/me/ - get current user
- PATCH /api/users/me/ - update current user

### Todos
- GET /api/todos/ - list todos for the authenticated user
- POST /api/todos/ - create a todo
- GET /api/todos/<id>/ - get a todo
- PATCH /api/todos/<id>/ - update a todo
- DELETE /api/todos/<id>/ - delete a todo
- PATCH /api/todos/<id>/toggle-done/ - mark a todo as done or undone

## API Documentation

Swagger UI is available at:

- http://127.0.0.1:8000/api/docs/

You can also view the raw schema at:

- http://127.0.0.1:8000/api/schema/


## Testing

Run tests with:

```bash
cd ./to-do-app/to_do_server
python manage.py test accounts
```
