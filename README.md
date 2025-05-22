# Job Tracker API

A FastAPI-based backend for tracking job applications, interviews, and notes.

## Features

- User authentication with JWT tokens
- CRUD operations for job applications
- Notes for each job application
- Secure password hashing
- SQLite database (can be configured for PostgreSQL)

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with the following content:
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./job_tracker.db
```

4. Run the application:
```bash
uvicorn backend.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:
- Interactive API documentation (Swagger UI): `http://localhost:8000/docs`
- Alternative API documentation (ReDoc): `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- POST `/api/v1/token` - Get access token
- POST `/api/v1/users/` - Create new user

### Jobs
- GET `/api/v1/jobs/` - List all jobs
- POST `/api/v1/jobs/` - Create new job
- GET `/api/v1/jobs/{job_id}` - Get job details
- PUT `/api/v1/jobs/{job_id}` - Update job
- DELETE `/api/v1/jobs/{job_id}` - Delete job

### Job Notes
- POST `/api/v1/jobs/{job_id}/notes/` - Add note to job
- GET `/api/v1/jobs/{job_id}/notes/` - List job notes

## Security

- All endpoints except user creation and token generation require authentication
- Passwords are hashed using bcrypt
- JWT tokens are used for authentication
- CORS is configured to allow cross-origin requests (configure appropriately for production)

## Database

The application uses SQLite by default. To use PostgreSQL:

1. Update the DATABASE_URL in .env:
```
DATABASE_URL=postgresql://user:password@localhost/dbname
```

2. Install psycopg2-binary:
```bash
pip install psycopg2-binary
``` 