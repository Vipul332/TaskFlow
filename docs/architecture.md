# TaskFlow – System Architecture

## 1. Overview

TaskFlow follows a three-tier architecture consisting of:

1. Frontend – Next.js and TypeScript
2. Backend – Flask REST API
3. Database – Supabase PostgreSQL

The frontend communicates with the backend through HTTP requests. The backend handles authentication, validation, business logic, database operations, and Gmail notifications.

## 2. High-Level Architecture

```text
                 USER
                  |
                  v
        NEXT.JS FRONTEND
        (React + TypeScript)
                  |
           HTTP / REST API
                  |
                  v
           FLASK BACKEND
                  |
        +---------+----------+
        |         |          |
        v         v          v
   AUTH SERVICE TASK SERVICE NOTIFICATION SERVICE
        |         |          |
        v         v          v
   GOOGLE OAUTH  TASK       GMAIL API
                 OPERATIONS      |
        |         |              v
        +---------+         EMAIL DELIVERY
                  |
                  v
          SUPABASE POSTGRESQL
                  |
          USERS / TASKS /
          ACTIVITY LOGS /
          NOTIFICATIONS
```

## 3. Frontend Architecture

The frontend is developed using Next.js, React, TypeScript, and Tailwind CSS.

Responsibilities:

- Render the login and dashboard interfaces.
- Handle Google authentication through Google Identity Services.
- Display team members and tasks.
- Provide task creation and assignment functionality.
- Allow users to update task statuses.
- Communicate with backend API endpoints.
- Maintain frontend loading, success, and error states.

API requests include credentials so the browser can send the authentication session cookie.

## 4. Backend Architecture

The backend uses Flask and follows a layered architecture.

### Routes Layer

Handles HTTP requests, authentication requirements, request parsing, and API responses.

### Services Layer

Contains business logic, including:

- Google token verification.
- User creation and updates.
- Task validation and creation.
- Task status updates.
- Notification workflows.

### Repositories Layer

Responsible for communicating with Supabase PostgreSQL.

### Middleware Layer

Protects restricted endpoints by validating the signed session cookie.

### Extensions and Configuration

Initialize shared services such as the Supabase client and application configuration.

## 5. Authentication Flow

1. The user selects Google Login.
2. Google Identity Services provides an ID token.
3. The frontend sends the token to the Flask authentication endpoint.
4. The backend verifies the token using Google's authentication libraries.
5. The backend creates or updates the corresponding user record in Supabase.
6. The backend generates a signed session cookie.
7. The browser stores the cookie as HttpOnly.
8. Protected API requests use the session cookie to identify the authenticated user.

## 6. Task Management Flow

### Creating a Task

1. The user fills out the task form.
2. The frontend sends task details to the backend.
3. The backend validates the title, description, priority, and assignee.
4. The task service saves the task in Supabase.
5. If an assignee exists, the notification service sends an assignment email.
6. The frontend refreshes the task list.

### Updating Task Status

1. The user changes a task status.
2. The frontend sends a PATCH request.
3. The backend checks the task and user permissions.
4. The task repository updates the status.
5. If the status becomes COMPLETED, the backend notifies the task creator.
6. The updated task is returned to the frontend.

## 7. Email Notification Architecture

TaskFlow uses the Gmail API to send email notifications.

Two notification events are supported:

- TASK_ASSIGNED: Sent to the task assignee.
- TASK_COMPLETED: Sent to the task creator.

Notification processing:

1. A notification record is created with PENDING status.
2. The Gmail API sends the email.
3. On success, the record is updated to SENT.
4. On failure, the record is updated to FAILED with an error message.

Notification failures are logged and should not normally prevent a successfully created or updated task from being returned.

## 8. Database Architecture

Supabase PostgreSQL stores the application's persistent data.

Main tables:

- users
- tasks
- activity_logs
- notifications

Relationships are maintained using UUID primary keys and foreign keys.

See `database-schema.md` for details.

## 9. Security Considerations

- Google ID tokens are verified by the backend.
- Session cookies are HttpOnly.
- Backend routes enforce authentication.
- Task updates check whether the user is the task creator or assignee.
- Secret credentials are stored in environment variables.
- Supabase database access is performed from the backend.
- Production deployment must use HTTPS, secure cookie settings, strict CORS origins, and appropriate CSRF protection.

## 10. Deployment Architecture

Planned deployment:

- Frontend: Vercel
- Backend: Render
- Database: Supabase
- Email: Gmail API

The frontend communicates with the deployed backend through its configured API URL.
