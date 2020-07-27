# pricepredictor

Price predictor using django

# Steps Before running this project in your machine

1.  install python3
2.  install Django framework using pip3 `pip3 install Django`
3.  install mathfilters library using pip3 `pip3 install mathfilters`
4.  install coverage library using pip3 `pip3 install coverage` to generate coverage report of unit test
5.  create a directory using `mkdir fuelpricepredictor`
6.  start a project using `django-admin startproject fuelpricepredictor`
7.  go to project directory using `cd fuelpricepredictor`
8.  start the sub project using `python3 manage.py startapp mainapp`

After creating any database model, migrate the model using following commands.
`python3 manage.py makemigrations` to generate migration script files
`python3 manage.py migrate` to migrate the migration scripts
run the scripts of scipts folder
`python3 manage.py sqlmigrate mainapp 0001_initial` to migrate specific migration files

Run `python3 manage.py createsuperuser` to create Django superuser

Run `python3 manage.py test mainapp/tests.py` to run unit tests
Run `coverage run python3 manage.py test mainapp/tests.py` to run uni tests and generate coverage reports
