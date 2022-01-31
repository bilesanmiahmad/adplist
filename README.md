# ADPList Backend Project

This is a take home project from ADPList for the role of a Backend Django Engineer.

## Running the application locally

This project is dockerized to prevent any dependency failures. You will require Docker on your machine in order to run it or you can create a virtual environment and install the dependencies from the requirements.txt file.

### Running Project with Docker

1. Run `docker-compose up --build -d` in the project root folder.
2. Run the command `docker-compose exec web python manage.py migrate` to run migrations.
3. Run the command `docker-compose exec web python manage.py createsuperuser` to create a superuser that has permission to approve mentor profiles.
4. Test local server on `http://localhost:3000`.

### Testing the endpoints

All necessary endpoints and descriptions can be accessed at the Postman documentation [here](https://documenter.getpostman.com/view/1204879/UVeCRU2W)
