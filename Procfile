release: cd dom6modgen && python manage.py migrate
web: cd dom6modgen && gunicorn dom6modgen.wsgi --log-file -
worker: cd dom6modgen && celery -A dom6modgen worker -l info