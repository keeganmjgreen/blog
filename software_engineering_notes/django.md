# Django

[Django](https://docs.djangoproject.com/en/6.0/) is a web framework and a Python library for writing backend servers in Python for serving web apps.

A Django project usually contains multiple apps. Note: An app can be included in multiple projects and thus there is generally a many-to-many relationship between projects and apps.

## The `manage.py` Command-Line Tool

`manage.py` is used as a command-line tool for managing a Django project.

- `python manage.py runserver` runs a server for the project.

- `python manage.py startapp <app-name>` adds an empty app to the project.

- `python manage.py migrate` ensures that the database schema matches what is required by `settings.INSTALLED_APPS`, e.g., ensuring the `django_admin_log` table for the `django.contrib.admin` app.

- `python manage.py makemigrations <app-name>` stores model changes (including creation of new models) in `<app-name>/migrations/<file-name>.py*`.

- `python manage.py sqlmigrate <app-name> <migration-number>` prints the SQL commands corresponding to a migration.

- `python manage.py migrate` executes SQL commands to apply all migrations since the latest one, e.g., `CREATE TABLE`, `CREATE INDEX`, etc. in a transaction. The latest migration is stored in `django_migrations`. This effectively syncs the database schema to the project's models.

## HTTP Request Handling

`urlpatterns` in an *app*'s `urls.py` file maps URL routes to handler functions defined in `views.py`, each of which takes an `HttpRequest`, does something, and returns an `HttpResponse`.

`urlpatterns` in the *project*'s `urls.py` file maps high-level URL routes to the `urlpatterns` defined for a specific app.

## Database Integration

The default database is SQLite, but it is not scalable/production-ready. PostgreSQL, MariaDB, MySQL, and Oracle databases are supported.

A project's database table schemas and relationships are defined by SQLAlchemy-like models in `models.py` *first*, from which `python manage.py migrate` is used to create the tables or update their schemas.

Django includes an ORM.

## Miscellaneous

ASGI- or WSGI-compatible servers (e.g., Apache) should be used for production.
