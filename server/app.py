from datetime import datetime
from flask import Flask, jsonify, request
from flask_migrate import Migrate

from models import Exercise, Workout, WorkoutExercises, db
from schemas import ExerciseSchema, WorkoutExercisesSchema, WorkoutSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExercisesSchema()

db.init_app(app)

@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200

@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
  workout = Workout.query.get(id)
  if not workout:
    return jsonify({"error": "Workout not found"}), 404
  return jsonify(workout_schema.dump(workout)), 200

@app.route("/workouts", methods=["POST"])
def create_workout():
    pass

@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    pass

@app.route("/exercises", methods=["GET"])
def get_exercises():
    pass

@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    pass

@app.route("/exercises", methods=["POST"])
def create_exercise():
    pass

@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    pass

@app.route("/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",methods=["POST"])
def add_exercise_to_workout(workout_id, exercise_id):
    pass

if __name__ == '__main__':
    app.run(port=5555, debug=True)