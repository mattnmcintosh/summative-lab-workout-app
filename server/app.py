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
  data = request.get_json() or {}
  try:
    validated_data = workout_schema.load(data)

    new_workout = Workout(
        date=validated_data.get("date"),
        duration_minutes=validated_data.get("duration_minutes"),
        notes=validated_data.get("notes"),
    )
    db.session.add(new_workout)
    db.session.commit()
    return jsonify(workout_schema.dump(new_workout)), 201
  except Exception as e:
    db.session.rollback()
    return jsonify({"error": e.messages if hasattr(e, "messages") else str(e)}), 400

@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
  workout = Workout.query.get(id)
  if not workout:
    return jsonify({"error": "Workout not found"}), 404

  db.session.delete(workout)
  db.session.commit()
  return jsonify({"message": "Workout deleted successfully"}), 200

def get_exercises():
  exercises = Exercise.query.all()
  return jsonify(exercises_schema.dump(exercises)), 200

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