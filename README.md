# Finance Manager API

A FastAPI-based financial management application that helps users track their income and expenses.

## Features

- User management
- Transaction tracking (income and expenses)
- PostgreSQL database integration
- Docker support
- CI/CD with GitHub Actions

## Prerequisites

- Python 3.11+
- PostgreSQL
- Docker (optional)

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd <your-repo-name>
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your database configuration:
```
POSTGRES_USER=coach_admin
POSTGRES_PASSWORD=finCoach_2025!
POSTGRES_DB=fincoach_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

## Running the Application

### Using Python directly:

```bash
uvicorn app.main:app --reload
```

### Using Docker:

```bash
docker build -t finance-app .
docker run -p 8000:8000 finance-app
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:
- Swagger UI documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## API Endpoints

### Users
- POST `/users/` - Create a new user
- GET `/users/{user_id}` - Get user details

### Transactions
- POST `/users/{user_id}/transactions/` - Create a new transaction
- GET `/users/{user_id}/transactions/` - Get all transactions for a user
- GET `/transactions/{transaction_id}` - Get transaction details
- PUT `/transactions/{transaction_id}` - Update a transaction
- DELETE `/transactions/{transaction_id}` - Delete a transaction 