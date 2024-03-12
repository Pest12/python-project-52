# Task manager


### Hexlet tests and linter status:
[![Actions Status](https://github.com/Pest12/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Pest12/python-project-52/actions)
[![Project2 check](https://github.com/Pest12/python-project-52/actions/workflows/project4-test.yml/badge.svg)](https://github.com/Pest12/python-project-52/actions/worklows/project4-test.yml)
[![Test Coverage](https://api.codeclimate.com/v1/badges/e6688c17537f23e525e7/test_coverage)](https://codeclimate.com/github/Pest12/python-project-52/test_coverage)
[![Maintainability](https://api.codeclimate.com/v1/badges/e6688c17537f23e525e7/maintainability)](https://codeclimate.com/github/Pest12/python-project-52/maintainability)

## Description


Task Manager is a task management system similar to http://www.redmine.org /. It allows you to set tasks, assign performers and change their statuses.


## Installation


Clone the repository `git clone git@github.com:Pest12/python-project-52.git` and use this commands:

```
make build
make start
```


##Link to Render.com: https://task-manager-app-hudw.onrender.com/


## Development server


To run the site locally on the development server, you need to:
- Create a file `.env` based on `.env.sample` `cp .env.sample .env`
- Fill `DATABASE_URL` and `SECRET_KEY` in .env
- Run `make dev`