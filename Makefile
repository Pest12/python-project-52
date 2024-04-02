run_server:
	poetry run python manage.py runserver

makemigrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate

install:
	poetry install

lint:
	poetry run flake8 task_manager

test:
	poetry run coverage run manage.py test

test-coverage:
	poetry run coverage xml

show-test-coverage:
	poetry run coverage report

PORT ?= 8000
WEB_CONCURRENCY ?= 4
start:
	poetry run gunicorn -w $(WEB_CONCURRENCY) -b 0.0.0.0:$(PORT) task_manager.wsgi:application

build:
	make install
	./build.sh