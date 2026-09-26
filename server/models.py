from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()

class Exercise(db.Model):
  __tablename__ = "exercises"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  category = db.Column(db.String)
  equipment_needed = db.Column(db.Boolean, default=False)

  # Relationship to the join table (WorkoutExercises)
  workout_exercises = db.relationship("WorkoutExercises",back_populates="exercise",cascade="all, delete-orphan")

  workouts = association_proxy('workout_exercises', 'workout')

  def __repr__(self):
    return (f"<Exercise id={self.id}, name='{self.name}',"f" category='{self.category}'>")

class Workout(db.Model):
  __tablename__ = "workouts"

  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.Date, nullable=False)
  duration_minutes = db.Column(db.Integer)
  notes = db.Column(db.Text)

  # Relationship to the join table (WorkoutExercises)
  workout_exercises = db.relationship("WorkoutExercises", back_populates="workout", cascade="all, delete-orphan")

  exercises = association_proxy('workout_exercises', 'exercise')

  def __repr__(self):
    return f"<Workout id={self.id}, date='{self.date}'>"

class WorkoutExercises(db.Model):
  __tablename__ = "workout_exercises"

  id = db.Column(db.Integer, primary_key=True)
  workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
  exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)
  reps = db.Column(db.Integer)
  sets = db.Column(db.Integer)
  duration_seconds = db.Column(db.Integer)

  # Relationships back to Workout and Exercise
  workout = db.relationship("Workout", back_populates="workout_exercises")
  exercise = db.relationship("Exercise", back_populates="workout_exercises")

  def __repr__(self):
    return (
        f"<WorkoutExercises id={self.id}, workout_id={self.workout_id},"f" exercise_id={self.exercise_id}>")