web: gunicorn --chdir dom6modgen dom6modgen.wsgi:application --log-file -
web: gunicorn dom6modgen.wsgi --timeout 120 --log-file -
worker: celery -A dom6modgen worker --loglevel=info