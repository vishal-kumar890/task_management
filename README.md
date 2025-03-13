# Task Management API

A RESTful API for managing tasks, built with Django and Django REST Framework.

# Overview
This Task Management API allows users to create, read, update, and delete tasks. Tasks can be assigned to users, filtered by status, and have rate-limited endpoints for protection against abuse.

# Features

## CRUD Operations: Complete task management capabilities
- **User Authentication**: Token-based authentication
- **Task Filtering**: Filter tasks by status and other properties
- **Rate Limiting**: API rate limiting to prevent abuse
- **AWS Integration**: Simulated Lambda function for task completion notifications
- **Unit Tests**: Comprehensive test coverage

# Tech Stack

- **Framework**: Django & Django REST Framework
- **Database**: PostgreSQL (compatible with AWS Aurora)
- **Caching**: Redis for rate limiting
- **AWS Integration**: Simulated Lambda function

# API Endpoints

## Authentication

- **POST /api/token/** - Obtain an authentication token

## Tasks

- **GET /api/tasks/** - List all tasks (filtered to those created by or assigned to the authenticated user)
- **POST /api/tasks/** - Create a new task
- **GET /api/tasks/<id>/** - Retrieve a specific task
- **PUT /api/tasks/<id>/** - Update a task
- **PATCH /api/tasks/<id>/** - Partially update a task
- **DELETE /api/tasks/<id>/** - Delete a task
- **GET /api/tasks/my_tasks/** - List tasks assigned to the authenticated user

## Filtering Examples

- **GET /api/tasks/?task_status=pending** - Get all pending tasks
- **GET /api/tasks/?task_status=completed** - Get all completed tasks
- **GET /api/tasks/?assigned_to=<user_id>** - Get tasks assigned to a specific user

# Setup Instructions
## Prerequisites

Python 3.8+
PostgreSQL
Redis (optional, for rate limiting)

# Environment Variables
Create a .env file in the project root with the following variables:

```
# Django
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True

# Database
DB_NAME=task_management
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://127.0.0.1:6379/1

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600

# AWS (simulated)
AWS_LAMBDA_FUNCTION_NAME=task-notification
AWS_REGION=us-east-1

```

# Installation

### Clone the repository:

```
git clone https://github.com/vishal-kumar890/task_management.git
cd task_management

```

### Create and activate a virtual environment:

```
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

```

### Install dependencies:

```
pip install -r requirements.txt

```

### Run migrations:

```
python manage.py migrate

```

### Create a superuser:

```
python manage.py createsuperuser

```

### Run the development server:

```
python manage.py runserver

```

# Design Choices

## Database Schema

The application uses Django's ORM with the following main models:
- **Task** : The core model representing a Task with fields for task_name, task_description, task_status, due_date, and foreign keys to the assigned user and creator.

- **RateLimitRecord** : Used to track API usage for rate limiting, with fields for user, endpoint, request count, and time window.

## Rate Limiting Implementation

Rate limiting is implemented using:

- Redis cache for fast in-memory tracking of request counts
- A database table for persistence and analytics
- A custom viewset mixin that can be applied to any API endpoint

This approach provides:

-    Efficient runtime performance using Redis
-    Historical data for analytics via the database
-    Flexibility to apply rate limiting to any endpoint

## AWS Integration

The application simulates AWS integration with:

- A function that mimics an AWS Lambda invocation when a task is marked as completed
- Environment variables for configuration
- Detailed logging for debugging

For a production environment, this would be replaced with actual AWS SDK calls.

## Auto-scaling Logic

The included pseudocode demonstrates how the application could be scaled in a production environment based on task volume.

## Testing

Run the tests with:

```
python manage.py test

```
