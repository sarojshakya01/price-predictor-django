# pricepredictor

Price predictor using django

# Steps Before running this project in your machine

1.  install python3
2.  install Django framework using pip3 `pip3 install Django`
3.  install mathfilters library using pip3 `pip3 install mathfilters`
4.  install coverage library using pip3 `pip3 install coverage` to generate coverage report of unit test
5.  run `pip3 install psycopg2` for postgres database connection
6.  run `pip3 install django-nose` for unit testing with coverage report
7.  run `pip3 install mathfilters` for front end maths operations
8.  create a directory using `mkdir fuelpricepredictor`
9.  start a project using `django-admin startproject fuelpricepredictor`
10. go to project directory using `cd fuelpricepredictor`
11. start the sub project using `python3 manage.py startapp mainapp`

# Running Server

- Run server using `python3 manage.py runserver`

# Migrtion Scripts

After creating any database model, migrate the model using following commands.

- `python3 manage.py makemigrations` to generate migration script files

- `python3 manage.py migrate` to migrate the migration scripts

- `python3 manage.py sqlmigrate mainapp 0001_initial` to migrate specific migration files

# Create States records

- run the scripts of scipts folder

# If you are using django user tables

- Run `python3 manage.py createsuperuser` to create Django superuser

# Unit Tests and coverage reports

- Run `python3 manage.py test mainapp/tests.py` to run unit tests
- Run `coverage run python3 manage.py test mainapp/tests.py` to run uni tests and generate coverage reports
