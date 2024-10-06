# Project Management System

## Setup

1. Clone the repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Run migrations: `python manage.py migrate`.
4. Create a superuser: `python manage.py createsuperuser`.
5. Start the server: `python manage.py runserver`.

## Endpoints

- `/api/register/`: Create Simple user
- `/api/token/`: Obtain JWT token.
- `/api/projects/`: Create, read,
- `/api/projects/{project-id}/`:update, delete projects.
- `/api/projects/{project-id}/add_user/`: Add member to the project
- `/api/tasks/`: Create, read,
- `/api/tasks/{task-id}/`:update, delete tasks.
