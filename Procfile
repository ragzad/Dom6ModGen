web: gunicorn dom6modgen.dom6modgen.wsgi:application --log-file -
worker: celery -A dom6modgen.dom6modgen.celery worker --loglevel=info
release: python dom6modgen/manage.py migrate