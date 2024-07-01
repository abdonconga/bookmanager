#!/bin/sh

python manage.py migrate
python manage.py runscript initial_data
exec "$@"
