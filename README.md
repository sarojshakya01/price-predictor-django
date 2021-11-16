# pricepredictor

Price predictor using django

# Steps Before running this project in your machine

1.  install python3
2.  install postgresql(optional)
3.  install Django framework using pip3 `pip3 install Django`
5.  install coverage library using pip3 `pip3 install coverage` to generate coverage report of unit test
6.  run `pip3 install psycopg2` for postgres database connection (if you are using postgresql)
7.  run `pip3 install django-nose` for unit testing with coverage report
8.  run `pip3 install django-mathfilters` for front end maths operations
9.  create a directory using `mkdir fuelpricepredictor`
10. start a project using `django-admin startproject fuelpricepredictor`
11. go to project directory using `cd fuelpricepredictor`
12. start the sub project using `python3 manage.py startapp mainapp`

# Database configuration

1.  create a role using `creare role rol_name with encrypted password pass_word;`
    for eg `creare role django with encrypted password ******;`
2.  create database database_name in your db server using `create database database_name;`
    for eg `create database pricepredicor;`
3.  grant all accees on newly created db for newly created role using `grant all on database database_name to rol_name;`
    for eg `grant all on database pricepredicor to django;`
4.  give login access to the newly created role using `alter role role_name with login;`
    for eg `alter role django with login;`

# Database Settings

- locate settings.py in fuelpricepredictor/fuelpricepredictor folder
- go to line 94
- put your dbname, role and password

# Migrtion Scripts

After creating any database model, migrate the model using following commands.

- connect to the postgres database server
- create a database 'pricepredictor' using `create database pricepredictor; commit;` or simply create from the GUI tool
- `python3 manage.py makemigrations` to generate migration script files
- `python3 manage.py migrate` to migrate the migration scripts
- `python3 manage.py sqlmigrate mainapp 0001_initial` to migrate specific migration files

# Create States records

- run the scripts of ./scipts folder
- uncomment the code ./mainapp/forms.py from line 26-29

# Running Server

- Run server using `python3 manage.py runserver`

# If you are using django user tables

- Run `python3 manage.py createsuperuser` to create Django superuser

# Unit Tests and coverage reports

- Run `python3 manage.py test mainapp/tests.py` to run unit tests
- Run `coverage run manage.py test mainapp/tests.py` to run uni tests and generate coverage reports
