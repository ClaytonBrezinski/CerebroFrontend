# CerebroFrontend
## Primary Project Requirements
* Python 3.5+
* Django 1.11
* Fabric 1.8
* Gunicorn 18.0
* Psycopg2 2.6
* Reportlab 3.4


## Installation/Running the App
1. Install the requirements using `pip install -r requirements.txt`
2. Migrate the django models so that they correctly exist in django using
   `python manage.py makemigrations accounts blogs core glucoses` then
   `python manage.py migrate --run-syncdb`
3. (Optional) Populate the database with some dummy data
`python manage.py loaddata ./fixtures/initial_glucoses_category_data.json`
`python manage.py loaddata ./fixtures/initial_glucoses_unit_data.json`
4. (Optional) Create a superuser for accessing the admin pages
`python manage.py createsuperuser` and follow the instructions on screen
5. You can then decide to run the server demo or in production mode (all locally)

    **a)** To run a local demo by using SQLite, use the **settings/localdemo.py** settings file
    **b)** To run a local production instance using PostgreSQL, use the **settings/local.py** settings file

6. Run the local web server with `python manage.py runserver --settings=settings.localdemo`
altering the --settings setting to your choice from #5