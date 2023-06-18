#!/bin/sh

# Apply database migrations
echo "Apply database migrations"
alembic upgrade head

# start bot
python main.py
