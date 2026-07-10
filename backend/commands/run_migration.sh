#!/bin/sh
set -eu

cd /app

alembic upgrade head

if [ "${SEED_DATABASE:-0}" = "1" ]; then
  update_existing_arg=""
  if [ "${SEED_UPDATE_EXISTING:-0}" = "1" ]; then
    update_existing_arg="--update-existing"
  fi

  python -m database.populate \
    --data-dir "${SEED_DATA_DIR:-/app/src/database/seed_data}" \
    --batch-size "${SEED_BATCH_SIZE:-1000}" \
    --default-password "${SEED_DEFAULT_PASSWORD:-SeedPassword123!}" \
    ${update_existing_arg}
fi
