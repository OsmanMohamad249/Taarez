#!/usr/bin/env bash
set -euo pipefail

# Run backend tests with an ephemeral Postgres container.
# - Reads DB credentials from `backend/tests/.env.test` (defaults used if missing)
# - Starts a Postgres container bound to localhost:5432
# - Waits for Postgres to be ready, runs pytest (PYTHONPATH=backend)
# - Stops and removes the container on exit

HERE="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="${HERE}/.."
ENV_FILE="${REPO_ROOT}/backend/tests/.env.test"

CONTAINER_NAME="qeyafa_test_postgres"
POSTGRES_IMAGE="postgres:15"

# Load defaults
POSTGRES_USER="test_user"
POSTGRES_PASSWORD="test_password"
POSTGRES_DB="test_db"

if [ -f "$ENV_FILE" ]; then
  # shellcheck disable=SC2046
  export $(grep -v '^#' "$ENV_FILE" | xargs)
  POSTGRES_USER=${POSTGRES_USER:-$POSTGRES_USER}
  POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-$POSTGRES_PASSWORD}
  POSTGRES_DB=${POSTGRES_DB:-$POSTGRES_DB}
fi

echo "Using Postgres container: $CONTAINER_NAME"

function cleanup() {
  echo "Cleaning up Postgres container..."
  docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
}

trap cleanup EXIT

# If container already exists, remove it (stale)
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
  echo "Removing existing container ${CONTAINER_NAME}"
  docker rm -f "$CONTAINER_NAME"
fi

echo "Starting Postgres container (localhost:5432) ..."
docker run -d \
  --name "$CONTAINER_NAME" \
  -e POSTGRES_USER="$POSTGRES_USER" \
  -e POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \
  -e POSTGRES_DB="$POSTGRES_DB" \
  -p 5432:5432 \
  $POSTGRES_IMAGE >/dev/null

echo "Waiting for Postgres to be ready..."
RETRIES=0
MAX_RETRIES=60
SLEEP=1
while true; do
  if docker logs "$CONTAINER_NAME" 2>&1 | grep -q "database system is ready to accept connections"; then
    echo "Postgres ready"
    break
  fi
  RETRIES=$((RETRIES+1))
  if [ $RETRIES -ge $MAX_RETRIES ]; then
    echo "Postgres did not become ready in time (logs):"
    docker logs "$CONTAINER_NAME" || true
    exit 1
  fi
  sleep $SLEEP
done

echo "Running pytest (this may take a while)"
# Export env so backend code picks up test settings
export DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:5432/${POSTGRES_DB}"
export POSTGRES_USER POSTGRES_PASSWORD POSTGRES_DB

# Run tests (adjust pytest args as needed)
PYTHONPATH=backend pytest -q "$@"

echo "Tests finished"
