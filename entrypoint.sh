#!/bin/sh


# python manage.py flush --no-input
python manage.py migrate
python manage.py import_pokemon
python manage.py collectstatic --no-input
exec "$@"