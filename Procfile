web: gunicorn --chdir /app dom6modgen.dom6modgen.wsgi:application --timeout 120 --log-file -
worker: celery -A dom6modgen worker --loglevel=info