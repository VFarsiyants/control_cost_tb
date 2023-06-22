#!/bin/sh

# Apply database migrations
echo "Apply database migrations"
alembic upgrade head

# install fixtures
python manage.py loaddataall

# start bot
python main.py
