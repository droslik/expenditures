#!/bin/sh
#set -e
#
#if [ "$POSTGRES_DB" = 'innotter_db' ]; then
#    chown -R postgres "$PGDATA"
#
#    if [ -z "$(ls -A "$PGDATA")" ]; then
#        gosu postgres initdb
#    fi
#
#    exec gosu postgres "$@"
#fi
#
#exec "$@"


#until nc -z -v -w30 "$POSTGRESQL_HOST" "$POSTGRESQL_PORT"
#do
#    echo "Waiting for a database..."
#    sleep 0.5
#done
sleep 5
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
