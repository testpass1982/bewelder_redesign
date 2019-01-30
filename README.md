## This is documentation for bewelder_redesign learning project

Documentation file will be here...

[Link for online google_docs (in Russian)](https://docs.google.com/document/d/10kYOiEE8X2aqLmEdEEs0LTF1ZPBDxLFZ_V0NUbQDIqI/)

Running **dev-server** of the project:
1. git clone https://github.com/testpass1982/bewelder_redesign
2. git checkout -b dev origin/dev
3. python manage.py makemigrations
4. python manage.py migrate
5. python manage.py createsuperuser
6. email: admin@admin.ru, first name: your_name, last_name: your_last_name
7. password: your_password
8. python manage.py runserver
9. visit http://localhost:8000 (or  http://127.0.0.1:8000)

Running **gulp-compilation** and **browser-sync**:
1. cd /bewelder_redesign (project root folder with manage.py)
2. gulp watch
3. visit http://127.0.0.1:8000 (or link, that shown in console)