# PostgreSQL setup

This Django project has been converted from MySQL to PostgreSQL.

## 1. Install PostgreSQL

Create a PostgreSQL database and user. For local development, the defaults used by this project are:

- Database: `banking_system`
- User: `postgres`
- Password: `1234`
- Host: `localhost`
- Port: `5432`

You can use different values by setting the `POSTGRES_*` environment variables.

## 2. Install Python dependencies

From this project directory:

```bash
python -m pip install -r requirements.txt
```

The MySQL drivers (`mysqlclient` and `PyMySQL`) have been removed. The PostgreSQL driver is `psycopg[binary]`.

## 3. Create the database

Using `psql`:

```sql
CREATE DATABASE banking_system;
```

If your PostgreSQL installation already has a suitable `postgres` user, no additional user creation is required.

## 4. Apply Django migrations

Run:

```bash
python manage.py migrate
```

The existing Django migrations are database-independent, so they do not need to be rewritten just because the backend changed from MySQL to PostgreSQL.

## 5. Create an admin user

```bash
python manage.py createsuperuser
```

## 6. Start the application

```bash
python manage.py runserver
```

## Important

If the old MySQL database contains data that you need to keep, do **not** simply run migrations against PostgreSQL and expect the data to appear. The PostgreSQL database starts empty. MySQL data must be migrated separately (for example, by exporting/importing the data or using a database migration tool).

For a fresh PostgreSQL database, `python manage.py migrate` is the correct approach.
