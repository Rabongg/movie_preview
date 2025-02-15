REDIS_HOST=redis
REDIS_PORT=6379

* * * * * /usr/bin/python3 /app/main.py >> /var/log/cron.log 2>&1
