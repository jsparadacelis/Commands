build:
	docker build .

up:
	docker-compose up --build

down:
	docker-compose down

unit:
	docker-compose run web pytest
