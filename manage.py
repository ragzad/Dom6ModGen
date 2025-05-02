#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path # Import Path

def main():
    """Run administrative tasks."""
    # Get the path to the directory containing the inner project package (dom6modgen)
    # __file__ is manage.py, resolve().parent gets its directory (/app on Heroku)
    # / 'dom6modgen' appends the inner project directory name
    inner_project_dir = Path(__file__).resolve().parent / 'dom6modgen'

    # Insert this directory at the beginning of sys.path
    # This allows Python to find modules/packages within the inner dom6modgen directory
    if str(inner_project_dir) not in sys.path:
         sys.path.insert(0, str(inner_project_dir))

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dom6modgen.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Couldn't import Django. "
            
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dom6modgen.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. "
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
