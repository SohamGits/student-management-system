#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mycore.settings')
    production_settings = (
        "SECRET_KEY",
        "ALLOWED_HOSTS",
        "DATABASE_URL",
        "REDIS_URL",
        "RENDER",
        "RENDER_EXTERNAL_HOSTNAME",
    )
    if "DEBUG" not in os.environ and not any(
        name in os.environ for name in production_settings
    ):
        os.environ["DEBUG"] = "true"

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
