up:
	sudo docker compose up
build:
	sudo docker compose build
makemig:
	sudo docker compose exec web-app python3 manage.py makemigrations
mig:
	sudo docker compose exec web-app python3 manage.py migrate
superuser:
	sudo docker compose exec web-app python3 manage.py createsuperuser