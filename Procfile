release: python manage.py migrate && python manage.py collectstatic --noinput
web: gunicorn dom6modgen.wsgi --log-file -
worker: celery -A dom6modgen worker -l info