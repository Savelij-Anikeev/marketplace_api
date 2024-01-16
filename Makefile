up:
	sudo docker compose up
build:
	sudo docker compose build
makemig:
	sudo docker compose run --rm web-app sh -c "python3 manage.py makemigrations"
mig:
	sudo docker compose run --rm web-app sh -c "python3 manage.py migrate"
superuser:
	sudo docker compose run --rm web-app sh -c "python3 manage.py createsuperuser"