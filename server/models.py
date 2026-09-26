from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from marshmallow import Schema, fields, validate

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

  @validates("name")
  def validate_name(self, key, name):
    if not name or not name.strip():
      raise ValueError("Exercise must have a valid name.")
    return name

  @validates("category")
  def validate_category(self, key, category):
    allowed_categories = ["Cardio", "Strength", "Flexibility", "Balance"]
    if category and category not in allowed_categories:
      raise ValueError(f"Category must be one of: {allowed_categories}")
    return category

  def __repr__(self):
    return (f"<Exercise id={self.id}, name='{self.name}',"f" category='{self.category}'>")

class ExerciseSchema(Schema):
  id = fields.Int(dump_only=True)
  name = fields.Str(required=True, validate=validate.Length(min=1))
  category = fields.Str(validate=validate.OneOf(["Cardio", "Strength", "Flexibility", "Balance"],error="Category must be one of: Cardio, Strength, Flexibility, Balance",))
  equipment_needed = fields.Bool()

  # Exclude 'exercise' inside workout_exercises to prevent recursion
  workout_exercises = fields.Nested("WorkoutExercisesSchema", many=True, exclude=("exercise",))

class Workout(db.Model):
  __tablename__ = "workouts"

  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.Date, nullable=False)
  duration_minutes = db.Column(db.Integer)
  notes = db.Column(db.Text)

  # Relationship to the join table (WorkoutExercises)
  workout_exercises = db.relationship("WorkoutExercises", back_populates="workout", cascade="all, delete-orphan")

  exercises = association_proxy('workout_exercises', 'exercise')

  __table_args__ = (CheckConstraint("duration_minutes > 0", name="check_duration_minutes_positive"),)

  def __repr__(self):
    return f"<Workout id={self.id}, date='{self.date}'>"

class WorkoutSchema(Schema):
  id = fields.Int(dump_only=True)
  date = fields.Date(required=True)
  duration_minutes = fields.Int(validate=validate.Range(min=1, error="Duration must be at least 1 minute."))
  notes = fields.Str()

  # Exclude 'workout' inside workout_exercises to prevent recursion
  workout_exercises = fields.Nested("WorkoutExercisesSchema", many=True, exclude=("workout",))

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

  __table_args__ = (CheckConstraint("reps >= 0", name="check_reps_non_negative"),)

  def __repr__(self):
    return (
        f"<WorkoutExercises id={self.id}, workout_id={self.workout_id},"f" exercise_id={self.exercise_id}>")

class WorkoutExercisesSchema(Schema):
  id = fields.Int(dump_only=True)
  workout_id = fields.Int(required=True)
  exercise_id = fields.Int(required=True)
  reps = fields.Int(validate=validate.Range(min=0, error="Reps cannot be negative."))
  sets = fields.Int(validate=validate.Range(min=0, error="Sets cannot be negative."))
  duration_seconds = fields.Int(validate=validate.Range(min=0, error="Duration seconds cannot be negative."))

  # Nest parent models without triggering recursive loops
  workout = fields.Nested("WorkoutSchema", exclude=("workout_exercises",))
  exercise = fields.Nested("ExerciseSchema", exclude=("workout_exercises",))