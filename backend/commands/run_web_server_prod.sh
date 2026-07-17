#!/bin/sh

set -e

# Run migrations
alembic upgrade head

# Run web server
uvicorn main:app --host 0.0.0.0 --port 8000
