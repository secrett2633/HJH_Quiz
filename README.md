# Quiz API

flowchart TD
    Clients["Client Applications"]:::client

    subgraph "API Layer"
        API["API Endpoints (backend/api/v1)"]:::api
    end

    subgraph "Service Layer"
        SERVICE["Business Logic (backend/services)"]:::service
    end

    subgraph "Data Access Layer"
        CRUD["CRUD Operations (backend/crud)"]:::crud
        ORM["ORM Models (backend/models)"]:::orm
        MIGR["DB Migrations (backend/models/migrations)"]:::orm
    end

    subgraph "External Services"
        PG[(PostgreSQL Database)]:::ext
        REDIS["Redis Cache"]:::ext
    end

    subgraph "Core & Utilities"
        CORE["Core Config (backend/core)"]:::core
        UTILS["Utilities (backend/utils)"]:::core
    end

    subgraph "Infrastructure Components"
        DOCKERFILE["Dockerfile"]:::infra
        DOCKERCOMPOSE["docker-compose.yml"]:::infra
        GUNICORN["gunicorn.conf.py"]:::infra
    end

    %% Main data flow
    Clients -->|"HTTP Request"| API
    API -->|"routes to"| SERVICE
    SERVICE -->|"calls"| CRUD
    CRUD -->|"uses"| ORM
    ORM -->|"maps to"| PG
    SERVICE -->|"caches with"| REDIS

    %% Supporting utilities
    API -.->|"uses"| CORE
    API -.->|"uses"| UTILS
    SERVICE -.->|"uses"| CORE
    SERVICE -.->|"uses"| UTILS
    CRUD -.->|"config via"| CORE

    %% Deployment relation
    DOCKERCOMPOSE ---|"deploys"| API
    DOCKERCOMPOSE ---|"deploys"| SERVICE
    DOCKERCOMPOSE ---|"deploys"| CRUD

    %% Link migrations to ORM (for schema updates)
    ORM ---|"maintains"| MIGR

    %% Click Events
    click API "https://github.com/secrett2633/hjh_quiz/tree/main/backend/api/v1"
    click SERVICE "https://github.com/secrett2633/hjh_quiz/tree/main/backend/services"
    click CRUD "https://github.com/secrett2633/hjh_quiz/tree/main/backend/crud"
    click ORM "https://github.com/secrett2633/hjh_quiz/tree/main/backend/models"
    click MIGR "https://github.com/secrett2633/hjh_quiz/tree/main/backend/models/migrations"
    click CORE "https://github.com/secrett2633/hjh_quiz/tree/main/backend/core"
    click UTILS "https://github.com/secrett2633/hjh_quiz/tree/main/backend/utils"
    click REDIS "https://github.com/secrett2633/hjh_quiz/blob/main/backend/utils/redis.py"
    click DOCKERFILE "https://github.com/secrett2633/hjh_quiz/tree/main/Dockerfile"
    click DOCKERCOMPOSE "https://github.com/secrett2633/hjh_quiz/blob/main/docker-compose.yml"
    click GUNICORN "https://github.com/secrett2633/hjh_quiz/blob/main/gunicorn.conf.py"

    %% Styles
    classDef client fill:#ffcc00,stroke:#333,stroke-width:2px
    classDef api fill:#a3d5ff,stroke:#333,stroke-width:2px
    classDef service fill:#d5f5aa,stroke:#333,stroke-width:2px
    classDef crud fill:#fff5ba,stroke:#333,stroke-width:2px
    classDef orm fill:#ffd6a5,stroke:#333,stroke-width:2px
    classDef ext fill:#ffb3b3,stroke:#333,stroke-width:2px
    classDef core fill:#d3d3d3,stroke:#333,stroke-width:2px
    classDef infra fill:#e0e0e0,stroke:#333,stroke-width:2px




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

