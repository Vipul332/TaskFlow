# TaskFlow – API Documentation

## 1. Overview

TaskFlow provides RESTful APIs using Flask.

Base URL (local):

```text
http://localhost:5000/api
```

Authentication uses a signed HTTP-only session cookie named `taskflow_session`.

Protected endpoints require a valid session cookie.

## 2. Authentication APIs

### 2.1 Google Login

**Endpoint:** `POST /auth/google`

**Purpose:** Verify a Google ID token and create or update the authenticated user.

Request body:

```json
{
  "credential": "GOOGLE_ID_TOKEN"
}
```

The credential field contains the Google ID token returned by Google Identity Services.

### 2.2 Get Current User

**Endpoint:** `GET /auth/me`

**Purpose:** Return the currently authenticated user's profile.

Authentication: Required.

### 2.3 Logout

**Endpoint:** `POST /auth/logout`

**Purpose:** Clear the authentication session cookie.

## 3. Task APIs

### 3.1 Get Tasks

**Endpoint:** `GET /tasks/`

Authentication: Required.

**Purpose:** Retrieve tasks where the authenticated user is the creator or assignee.

### 3.2 Create Task

**Endpoint:** `POST /tasks/`

Authentication: Required.

Request body:

```json
{
  "title": "Complete project documentation",
  "description": "Prepare API and database documentation",
  "priority": "HIGH",
  "assignee_id": "USER_UUID"
}
```

`assignee_id` can be null when the task is not assigned.

Supported priority values:

- LOW
- MEDIUM
- HIGH
- URGENT

**Purpose:** Create a task and send an assignment email when an assignee is selected.

### 3.3 Update Task Status

**Endpoint:** `PATCH /tasks/{task_id}/status`

Authentication: Required.

Request body:

```json
{
  "status": "COMPLETED"
}
```

Supported statuses:

- TODO
- IN_PROGRESS
- COMPLETED

Only the task creator or assignee can update the task status.

When the status changes to COMPLETED, an email notification is sent to the task creator.

## 4. User APIs

### 4.1 Get Team Members

**Endpoint:** `GET /users/`

Authentication: Required.

**Purpose:** Retrieve registered team members.

## 5. Health API

### 5.1 Backend Health Check

**Endpoint:** `GET /health`

**Purpose:** Check whether the backend service is running.

Example response:

```json
{
  "success": true,
  "message": "TaskFlow backend is running!",
  "service": "TaskFlow API"
}
```

## 6. Authentication and Authorization

- Google ID tokens are verified by the backend.
- A signed session cookie is issued after successful login.
- Protected endpoints validate the session cookie.
- Cookies are configured as HttpOnly.
- Task operations verify the user's relationship with the task.

## 7. Email Notification Events

| Event | Recipient | Notification Type |
|---|---|---|
| Task assigned | Assignee | TASK_ASSIGNED |
| Task completed | Task creator | TASK_COMPLETED |

Notification records are stored in the Supabase `notifications` table.

## 8. Common HTTP Status Codes

| Status | Meaning |
|---|---|
| 200 | Request successful |
| 201 | Resource created |
| 400 | Invalid request |
| 401 | Authentication required |
| 403 | Permission denied |
| 404 | Resource not found |
| 500 | Internal server error |

Exact response codes and JSON fields depend on the individual route implementation.

## 9. Local Development

Start the Flask backend:

```bash
python run.py
```

Start the Next.js frontend:

```bash
npm run dev
```

Frontend URL:

`http://localhost:3000`

Backend URL:

`http://localhost:5000`
