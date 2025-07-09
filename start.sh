#!/bin/bash

touch /var/log/cron.log

echo "File cron.log created..."

python /app/elt_script.py >> /var/log/cron.log 2>&1

cron

# python /app/elt_script.py

tail -f /var/log/cron.log