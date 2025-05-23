# Job Tracker API

A comprehensive FastAPI-based application for tracking job applications, interviews, and related activities. This application provides a robust backend API with features for user management, job tracking, and detailed logging.

## Features

- 🔐 **Authentication & Authorization**
  - JWT-based authentication
  - Role-based access control
  - Secure password hashing
  - Token-based session management

- 📝 **Job Management**
  - Create, read, update, and delete job applications
  - Track application status
  - Add notes and comments
  - Search and filter capabilities
  - Pagination support

- 🔍 **Advanced Features**
  - Database migrations with Alembic
  - Connection pooling
  - Request/response logging
  - Health check endpoints
  - GZip compression
  - CORS support
  - Input validation
  - Error handling

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite (configurable for other databases)
- **ORM**: SQLAlchemy
- **Authentication**: JWT
- **Migrations**: Alembic


## Prerequisites

- Python 3.8+
- pip (Python package manager)
- virtualenv (recommended)

## Installation

1. Clone the repository:
  
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows
   .\venv\Scripts\activate
   # On Unix or MacOS
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory with the following variables:
   ```
   DATABASE_URL=sqlite:///./job_tracker.db
   SECRET_KEY=your-secret-key
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   CORS_ORIGINS=["http://localhost:3000"]
   ALLOWED_HOSTS=["localhost", "127.0.0.1"]
   ```

5. Initialize the database:
   ```bash
   # Create initial migration
   alembic revision --autogenerate -m "Initial migration"
   
   # Apply migrations
   alembic upgrade head
   ```

## Running the Application

1. Start the development server:
   ```bash
   uvicorn backend.main:app --reload
   ```

2. Access the API documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/v1/token` - Get access token
- `POST /api/v1/users/` - Create new user

### Jobs
- `POST /api/v1/jobs/` - Create new job application
- `GET /api/v1/jobs/` - List all jobs (with filtering)
- `GET /api/v1/jobs/{job_id}` - Get specific job
- `PUT /api/v1/jobs/{job_id}` - Update job
- `DELETE /api/v1/jobs/{job_id}` - Delete job

### Job Notes
- `POST /api/v1/jobs/{job_id}/notes/` - Add note to job
- `GET /api/v1/jobs/{job_id}/notes/` - List job notes

### System
- `GET /health` - Health check endpoint
- `GET /` - API information

## Development

### Project Structure
```
job-tracker/
├── backend/
│   ├── alembic.ini
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── auth.py
│   ├── routes.py
│   └── migrations/
├── requirements.txt
└── README.md
```

### Database Migrations

To create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

To apply migrations:
```bash
alembic upgrade head
```

To rollback migrations:
```bash
alembic downgrade -1  # Rollback one migration
```

### Logging

The application uses Python's built-in logging module with the following configuration:
- Log level: INFO
- Output: Both file (app.log) and console
- Format: Timestamp - Logger Name - Level - Message

## Security Features

- Password hashing using bcrypt
- JWT token-based authentication
- CORS protection
- Trusted host middleware
- Input validation
- SQL injection protection through SQLAlchemy
- Secure session management

## Error Handling

The application includes comprehensive error handling:
- Global exception handler
- Validation error handler
- Database error handling
- Custom HTTP exceptions
- Detailed error logging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 