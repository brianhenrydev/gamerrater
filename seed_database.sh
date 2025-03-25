#!/bin/bash

rm db.sqlite3
rm -rf ./gamerraterapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations gamerraterapi
python3 manage.py migrate gamerraterapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens

python3 manage.py loaddata games
python3 manage.py loaddata categories
python3 manage.py loaddata game_players
python3 manage.py loaddata game_categories
python3 manage.py loaddata game_ratings
python3 manage.py loaddata game_review
