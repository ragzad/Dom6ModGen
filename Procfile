web: gunicorn wsgi:application --timeout 120 --log-file -
worker: celery -A celery worker --loglevel=info