#!/bin/sh

echo "Waiting for mysql..."

while ! nc -z $DB_HOST 3306; do
  sleep 0.1
done

echo "MySQL started"

python manage.py migrate

echo 'Django migration ready'

python manage.py collectstatic --no-input
echo 'Static ready'

# run server
echo 'UWSGI is working'
uwsgi --http "0.0.0.0:8000" --module project.wsgi --master --processes 4 --threads 2 --logto /tmp/lmnad.log
