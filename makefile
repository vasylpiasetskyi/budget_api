build:
	@docker-compose build

down:
	@docker-compose down

logs:
	@docker-compose logs -f $(c)

ps:
	@docker-compose ps

ssh:
	@docker-compose exec $(c) ash

stop:
	@docker-compose stop

start:
	@docker-compose up -d

start_:
	@docker-compose up

run:
	@docker-compose exec -d worker celery --workdir ./src/django/bella --app bella worker --loglevel INFO && docker-compose exec django python3 src/django/bella/manage.py runserver 0.0.0.0:8000

run_w:
	@docker-compose exec worker celery --workdir ./src/django/bella --app bella worker --loglevel INFO

run_:
	@docker-compose exec app python3 manage.py runserver 0.0.0.0:8000

bash:
	@docker-compose app /bin/bash

manage:
	@docker-compose exec app python3 manage.py $(c)

test:
	@docker-compose exec app python3 manage.py test $(c) -v 2
