https://docs.djangoproject.com/en/4.1/intro/tutorial02/

Activate environment for VS code
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

.venv\Scripts\activate.ps1


RUN DJANGO SERVER
python manage.py runserver

EXECUTE CHANGES TO MODELS
python manage.py makemigrations polls
python manage.py migrate


To perform calls to the model
python manage.py shell

TESTING
python manage.py test polls

