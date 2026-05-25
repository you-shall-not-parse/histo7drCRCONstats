#!/usr/bin/env bash

set -e
set -x

env

# Only run the database migrations in the maintenance container
if [ "$1" == 'maintenance' ]
then
  alembic upgrade head
  # Create this file after migrations which is how Docker determines the container is healthy
  touch maintenance-container-healthy
  # Keep the container running until it's explicitly created again
  sleep infinity
fi

# Check if we're in a backend container
if [ "$1" == 'web' ]
then
  # If the database password isn't set, bail early
  if [ "$HLL_DB_PASSWORD" == '' ]
  then
      echo "HLL_DB_PASSWORD not set"
      exit 0
  fi
  cd rconweb
  ./manage.py collectstatic --noinput
  export LOGGING_FILENAME=api_$SERVER_NUMBER.log
  # Successfully running gunicorn will create the pid file which is how Docker determines the container is healthy
  gunicorn --preload --pid gunicorn.pid -w $NB_API_WORKERS -k gthread --threads $NB_API_THREADS -t 120 -b 0.0.0.0 rconweb.wsgi
  cd ..
else
  if [ "$1" == 'debug' ]
  then
    tail -f manage.py
  fi
  exit 0
fi

