from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Exercise(db.Model):
  __tablename__ = "exercises"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  category = db.Column(db.String)
  equipment_needed = db.Column(db.Boolean, default=False)

  # Relationship to the join table (WorkoutExercises)
  workout_exercises = db.relationship("WorkoutExercises",back_populates="exercise",cascade="all, delete-orphan")

  # Optional association proxy to access workouts directly if desired
  # workouts = association_proxy('workout_exercises', 'workout')

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

  # Optional association proxy to access exercises directly if desired
  # exercises = association_proxy('workout_exercises', 'exercise')

  def __repr__(self):
    return f"<Workout id={self.id}, date='{self.date}'>"