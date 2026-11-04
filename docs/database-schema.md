# TaskFlow – Database Schema Documentation

## 1. Overview

TaskFlow uses Supabase PostgreSQL as its relational database.

The database stores user profiles, tasks, activity history, and email notification records.

All primary keys use UUIDs. Foreign keys maintain relationships between tables.

## 2. Database Tables

### 2.1 users

Stores users authenticated through Google OAuth.

| Column | Data Type | Constraints |
|---|---|---|
| id | UUID | Primary Key |
| google_id | TEXT | Unique, Not Null |
| name | TEXT | Not Null |
| email | TEXT | Unique, Not Null |
| avatar_url | TEXT | Nullable |
| created_at | TIMESTAMPTZ | Default NOW() |
| updated_at | TIMESTAMPTZ | Default NOW() |

### 2.2 tasks

Stores tasks created by users and assigned to team members.

| Column | Data Type | Constraints |
|---|---|---|
| id | UUID | Primary Key |
| title | VARCHAR(200) | Not Null |
| description | TEXT | Nullable |
| creator_id | UUID | FK → users.id |
| assignee_id | UUID | FK → users.id, Nullable |
| status | TEXT | TODO / IN_PROGRESS / COMPLETED |
| priority | TEXT | LOW / MEDIUM / HIGH / URGENT |
| due_date | TIMESTAMPTZ | Nullable |
| created_at | TIMESTAMPTZ | Default NOW() |
| updated_at | TIMESTAMPTZ | Default NOW() |

### 2.3 activity_logs

Stores historical actions performed on tasks.

| Column | Data Type | Constraints |
|---|---|---|
| id | UUID | Primary Key |
| task_id | UUID | FK → tasks.id |
| user_id | UUID | FK → users.id, Nullable |
| action | TEXT | Not Null |
| details | JSONB | Default empty JSON object |
| created_at | TIMESTAMPTZ | Default NOW() |

### 2.4 notifications

Stores email notification records and their delivery status.

| Column | Data Type | Constraints |
|---|---|---|
| id | UUID | Primary Key |
| task_id | UUID | FK → tasks.id |
| recipient_id | UUID | FK → users.id |
| type | TEXT | TASK_ASSIGNED / TASK_COMPLETED |
| status | TEXT | PENDING / SENT / FAILED |
| sent_at | TIMESTAMPTZ | Nullable |
| error_message | TEXT | Nullable |
| created_at | TIMESTAMPTZ | Default NOW() |

## 3. Entity Relationships

- One user can create multiple tasks.
- One user can be assigned multiple tasks.
- Each task has one creator.
- A task can have zero or one assignee.
- A task can have multiple activity log entries.
- A task can have multiple notification records.
- A user can receive multiple notifications.

## 4. Relationship Diagram

```text
USERS
  |
  |----< TASKS (creator_id)
  |
  |----< TASKS (assignee_id)
  |
  |----< ACTIVITY_LOGS
  |
  |----< NOTIFICATIONS

TASKS
  |
  |----< ACTIVITY_LOGS
  |
  |----< NOTIFICATIONS
```

## 5. Indexes

Indexes improve query performance.

The migrations create indexes for:

### Users
- email
- google_id

### Tasks
- creator_id
- assignee_id
- status
- created_at

### Activity Logs
- task_id
- user_id
- created_at

### Notifications
- recipient_id
- task_id
- status
- created_at

## 6. Referential Integrity

Foreign key constraints maintain consistency between related records.

- Deleting a user cascades deletion of tasks they created.
- Deleting an assignee sets the task assignee to NULL.
- Deleting a task cascades deletion of its activity logs and notifications.
- Deleting a user sets their activity log user reference to NULL.
- Deleting a user cascades deletion of their notification records.

## 7. Row Level Security

Row Level Security (RLS) is enabled on all four tables.

The backend uses a Supabase server-side secret key for database operations.

Because privileged server credentials can bypass RLS, the backend must enforce authentication and authorization for every protected operation.

The secret key must never be exposed in frontend code.

## 8. Database Migrations

Database migrations are maintained in `backend/migrations/`.

| Migration | Purpose |
|---|---|
| 001_create_users.sql | Creates users table |
| 002_create_tasks.sql | Creates tasks table |
| 003_create_activity_logs.sql | Creates activity_logs table |
| 004_create_notifications.sql | Creates notifications table |

Execute migrations in numerical order when setting up a new database.
