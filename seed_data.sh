#!/bin/bash

rm -rf bangazonapi/migrations
rm db.sqlite3
python manage.py makemigrations barsapi
python manage.py migrate
python manage.py loaddata users
python manage.py loaddata tokens
python manage.py loaddata barsusers
python manage.py loaddata playlists