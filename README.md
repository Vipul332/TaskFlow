# TaskFlow – Collaborative Task Management Platform

TaskFlow is a full-stack task management application that allows users to create tasks, assign tasks to team members, track task progress, and receive email notifications when tasks are assigned or completed.

## Features

- Google OAuth 2.0 authentication
- Create and manage tasks
- Assign tasks to registered team members
- Track task statuses:
  - TODO
  - IN_PROGRESS
  - COMPLETED
- Task priority levels:
  - LOW
  - MEDIUM
  - HIGH
  - URGENT
- Gmail API email notifications for task assignments and completion
- Notification history stored in Supabase PostgreSQL
- Team member listing
- Protected backend API endpoints

## Technology Stack

### Frontend
- Next.js
- React
- TypeScript
- Tailwind CSS

### Backend
- Python
- Flask
- Flask-CORS
- Google OAuth authentication
- Gmail API

### Database
- Supabase PostgreSQL

### Deployment
- Vercel (Frontend)
- Render (Backend)
- Supabase (Database)

## Project Structure

```text
TaskFlow/
├── backend/
│   ├── app/
│   ├── migrations/
│   ├── tests/
│   ├── credentials/
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── public/
│   ├── src/
│   └── package.json
├── docs/
│   ├── architecture.md
│   ├── database-schema.md
│   └── api-documentation.md
├── .gitignore
└── README.md
```

## Local Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd TaskFlow
```

### 2. Backend setup

```bash
cd backend
python -m venv venv
```

Activate the environment on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file using `.env.example` and configure the required credentials.

Start the backend:

```bash
python run.py
```

Backend runs at:

`http://localhost:5000`

### 3. Frontend setup

Open another terminal:

```bash
cd frontend
npm install
```

Create `.env.local` using `.env.example` and configure the Google Client ID and backend API URL.

Start the frontend:

```bash
npm run dev
```

Frontend runs at:

`http://localhost:3000`

## Database Setup

1. Create a Supabase PostgreSQL project.
2. Configure the backend environment variables.
3. Execute the SQL migration files in order:
   - `001_create_users.sql`
   - `002_create_tasks.sql`
   - `003_create_activity_logs.sql`
   - `004_create_notifications.sql`

## Email Notifications

TaskFlow integrates with the Gmail API to send:
- Task assignment notifications to the assignee.
- Task completion notifications to the task creator.

Gmail OAuth credentials must be configured securely in the backend environment.

## Documentation

Detailed documentation is available in the `docs/` directory:

- Architecture
- Database schema
- API documentation

## Security

- Secrets are stored in environment variables.
- Gmail OAuth credentials and tokens must never be committed.
- Backend API routes require authentication where appropriate.
- Task permissions are checked on the backend.

## Project Status

Core authentication, task management, assignment, status updates, and email notification workflows have been implemented and manually verified.

Automated tests and deployment documentation are being prepared.

## License

This project is available under the MIT License.
