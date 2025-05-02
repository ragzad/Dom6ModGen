release: cd Dom6ModGen/dom6modgen && python manage.py migrate
web: cd Dom6ModGen/dom6modgen && gunicorn dom6modgen.wsgi --log-file -
worker: cd Dom6ModGen/dom6modgen && celery -A dom6modgen worker -l info
