# Quiz API

## Requirements

* Python: ^3.10
* FastAPI: ^0.100.0

## Package
- python - Specifies the Python version requirement
- fastapi - High-performance web framework for building APIs with Python
- passlib - Password hashing library for secure password storage
- python-jose - Library for JWT token handling with cryptography extras
- pydantic - Data validation and settings management using Python type annotations, with email validation
- SQLAlchemy - SQL toolkit and ORM with mypy typing support
- asyncpg - High-performance PostgreSQL client library for asyncio
- phonenumbers - Library for parsing, formatting, and validating international phone numbers
- gunicorn - Python WSGI HTTP server for UNIX
- uvicorn - ASGI server implementation with standard extras
- toml - Library for parsing and writing TOML configuration files
- redis - Redis database client for caching and message brokering
- python-multipart - Parsing multipart/form-data, used for file uploads
- alembic - Database migration tool for SQLAlchemy
- greenlet - Lightweight coroutines for in-process concurrent programming
- bcrypt - Modern password hashing library for secure password storage
- loguru - Python logging library with a simple and powerful API

# Project Setup Guide

1. Install **Python** version **^3.10**.
2. Install **Poetry**, as dependency management is handled using Poetry.

## Running the Services

To easily run **PostgreSQL**, **Redis**, and the **backend server**, use Docker Compose:

```sh
docker compose up
```

## API Documentation

You can access the API documentation at:

```
http://localhost:8000/api/v1/docs
```

## User Registration

- Sign up via the following endpoint:
  
  ```
  POST /api/v1/auth/signup
  ```

- By default, the `is_superuser` (admin role) is set to `false`.
- You can update `is_superuser` to `true` using the following endpoint:
  
  ```
  PATCH /api/v1/users/{user_id}
  ```

