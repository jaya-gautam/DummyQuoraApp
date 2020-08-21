# Dummy Quora App
A Basic web application like Quora created using Django


## Features
* User can **signup, login & logout**
* User can **ask question**
* User can **answer question**
* User can **comment on answers**
* User can **upvote and downvote**


create and start a a virtual environment

```bash
virtualenv env --no-site-packages

source env/bin/activate
```

Install the python package requirements using `pip`.

```bash
pip install -r requirements.txt
```

Run the migrate command to create database tables.

```bash
python manage.py migrate
```

Use the `createsuperuser` command to create a user who has superuser privileges.

```bash
python manage.py createsuperuser
```

Finally run the server using the `runserver` command.

```bash
python manage.py runserver 0.0.0.0:8000
```
