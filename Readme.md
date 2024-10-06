# Project Management System

## Overview
This is a simple Project Management System API built using Django and Django REST Framework (DRF). The application allows users to:

Authenticate using JWT (JSON Web Tokens)
Create and manage projects
Add multiple users to projects
Perform CRUD operations on tasks within projects
Implement soft delete functionality for both projects and tasks
The project is designed to manage tasks associated with projects, including tracking the status and due dates of tasks, with authentication and permissions based on JWT.

> [!NOTE]
> As common practice SQLite3 database is not commited in repository, however I have commited SQLite3 database in repository for evidence of working project and you don't have to apply and run migrations. 

## Features
1. User Authentication:

JWT-based authentication.
Users can log in and get tokens to access the API.

2. Project Management:

Users can create projects with unique names and descriptions.
Users can add multiple members (users) to their projects.

3. Task Management:

Users can perform CRUD (Create, Read, Update, Delete) operations on tasks within their projects.
Each task has a title, description, status, and due date.

4. Soft Delete:

Projects and tasks are not physically deleted from the database but are marked as deleted (soft delete).

## Setup Instructions
### Prerequisites
Python 3.x
Django 5.1.1
Django REST Framework (DRF)
Django Simple JWT for token authentication
Postman (for testing API endpoints)

1. Clone the repository.
2. Create a Virtual Environment: `python -m venv myenv`
`source myenv/bin/activate   # On Windows, use `myenv\Scripts\activate``
3. Install dependencies using `pip install -r requirements.txt`.
4. Run migrations: `python manage.py migrate`.
5. Create a superuser (optional) : `python manage.py createsuperuser`.
6. Start the server: `python manage.py runserver`.
7. Access the Django Admin Panel:

Navigate to http://127.0.0.1:8000/admin to log in using your superuser credentials (available in userdetails.txt).

## Endpoints

- `/api/register/`: Create Simple user
- `/api/token/`: Obtain JWT token.
- `/api/projects/`: Create, read,
- `/api/projects/{project-id}/`:update, delete projects.
- `/api/projects/{project-id}/add_user/`: Add member to the project
- `/api/tasks/`: Create, read,
- `/api/tasks/{task-id}/`:update, delete tasks.



# Author
## Adil Sultan - Developer and Maintainer of this project.

