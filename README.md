🏋️‍♂️ Workout Tracker API
Project Description
The Workout Tracker API is a Flask-backed web service designed to manage fitness routines, exercises, and detailed workout metrics. It features relational database modeling with SQLAlchemy, robust data validation using Marshmallow schemas and database constraints, association proxies for clean many-to-many relationships, and a fully functional REST API.

Installation Instructions
Clone the repository and navigate into the project root directory:
cd server

Install dependencies using Pipenv:
pipenv install

Activate the virtual environment:
pipenv shell

Initialize and migrate the database:
flask db init
flask db migrate -m "initial migration"
flask db upgrade head

Seed the database with sample data:
python seed.py

Run Instructions
Start the development server using Flask:
python app.py
(Alternatively, you can run flask run --port 5555). The API will be accessible at http://localhost:5555.

API Endpoints
Workouts
GET /workouts

Description: Retrieves a list of all recorded workouts.

Response Status: 200 OK

GET /workouts/

Description: Retrieves a single workout along with its associated exercises and join-table metrics (reps, sets, duration).

Response Status: 200 OK (or 404 Not Found)

POST /workouts

Description: Creates a new workout record. Validates required date and positive duration values.

Response Status: 201 Created (or 400 Bad Request)

DELETE /workouts/

Description: Deletes a workout and its corresponding join-table entries.

Response Status: 200 OK (or 404 Not Found)

Exercises
GET /exercises

Description: Retrieves a list of all available exercises.

Response Status: 200 OK

GET /exercises/

Description: Retrieves a specific exercise and all past workouts it was included in.

Response Status: 200 OK (or 404 Not Found)

POST /exercises

Description: Creates a new exercise. Validates allowed categories (Cardio, Strength, Flexibility, Balance).

Response Status: 201 Created (or 400 Bad Request)

DELETE /exercises/

Description: Deletes an exercise from the catalog.

Response Status: 200 OK (or 404 Not Found)

Join Table Operations
POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises

Description: Associates an exercise with a specific workout, recording metrics like reps, sets, and duration in seconds.

Response Status: 201 Created (or 400/404 Error)

Pipfile Dependencies
This project relies on the following key Python packages managed via Pipenv:

flask

flask-sqlalchemy

flask-migrate

flask-marshmallow

marshmallow-sqlalchemy