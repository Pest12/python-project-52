run_server:
	poetry run python manage.py runserver

makemigrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate

install:
	poetry install

build:
	poetry build

lint:
	poetry run flake8 task_manager

test:
	poetry run coverage run manage.py test

test-coverage:
	poetry run coverage xml

show-test-coverage:
	poetry run coverage report
