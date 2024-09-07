# train-station API

API service for train station management written on DRF and Dockerized.

# Installing using GitHub

Install PostgresSQL and create db.
```bash
git clone https://github.com/kapitoshk4/train-station.git
cd train_station
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
set POSTGRES_USER=<your db username>
set POSTGRES_PASSWORD=<your db password>
set POSTGRES_DB=<your db name>
set POSTGRES_HOST=<your db hostname>
set SECRET_KEY=<your secret key>
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
python manage.py createsuperuser
```
# Run with docker

```bash
docker-compose build
docker-compose up
docker-compose ps
docker exec -it your_image_name sh
- Create new admin user. `docker-compose run app sh -c "python manage.py createsuperuser`;
- Run tests using different approach: `docker-compose run airport sh -c "python manage.py test"`;
```
# Getting access

To access the API endpoints, follow these steps:

1. Go to one if the following URLs:
   - [Login to obtain Token](http://127.0.0.1:8000/api/v1/user/register/) 
   - [Obtain Bearer token](http://127.0.0.1:8000/api/v1/user/token/)
2. Type your Email & Password. For example:
   - Email address: admin@admin.com
   - Password: 1qazcde3
3. After submitting your credentials, you will receive a token. This token grants access to the API endpoints.

# Available Endpoints For Users App

You can use the following endpoints:

- [Refresh Token](http://127.0.0.1:8000/api/v1/user/token/refresh/) - This URL will refresh your token when it expires.
- [Verify Token](http://127.0.0.1:8000/api/v1/user/token/verify/) - This URL will verify if your token is valid and has not expired.
- [User Details](http://127.0.0.1:8000/api/v1/user/me/) - This URL will display information about yourself using the token assigned to your user.

Please note that accessing certain endpoints may require the ModHeader extension, which is available for installation in Chrome.

That's it for user endpoints. You can now proceed to the next step.

# Getting Started With Api

1. First, go to the URL provided: [API Endpoints](http://127.0.0.1:8000/api/v1/station/). This URL provides all endpoints of the API.
2. Now you are ready to use the API to manage your train station.

# Features
- JWT authentication
- Admin panel available at /admin/
- Documentation located at /api/v1/doc/swagger/
- Manage orders and tickets for the train station
- Create Stations, Train Types, Trains (with images), Routes, Crew, Journeys, Orders, Tickets
- Implemented filtering for every endpoint in Swagger
- Filtering Routes by: Destination, Source
- Filtering Journeys by: Crew member id
- Filtering Trains by: Train type