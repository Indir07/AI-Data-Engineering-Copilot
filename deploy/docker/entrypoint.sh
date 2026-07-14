#!/usr/bin/env bash
# Container entrypoint: optionally apply DB migrations, then run the given command.
set -euo pipefail

if [ "${RUN_MIGRATIONS:-0}" = "1" ]; then
  echo "[entrypoint] Applying database migrations (alembic upgrade head)…"
  # Retry briefly in case Postgres is still accepting connections.
  for attempt in 1 2 3 4 5; do
    if alembic upgrade head; then
      break
    fi
    echo "[entrypoint] migration attempt ${attempt} failed; retrying in 3s…"
    sleep 3
  done
fi

echo "[entrypoint] Starting: $*"
exec "$@"
