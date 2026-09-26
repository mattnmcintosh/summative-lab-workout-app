#!/usr/bin/env python3
from datetime import date
from app import app
from models import db, Exercise, Workout, WorkoutExercises

with app.app_context():
  print("Deleting existing data...")
  WorkoutExercises.query.delete()
  Exercise.query.delete()
  Workout.query.delete()

  print("Creating exercises...")
  pushup = Exercise(
      name="Push-up", category="Strength", equipment_needed=False
  )
  running = Exercise(name="Running", category="Cardio", equipment_needed=False)
  squat = Exercise(name="Squat", category="Strength", equipment_needed=False)

  db.session.add_all([pushup, running, squat])
  db.session.commit()

  print("Creating workouts...")
  workout1 = Workout(
      date=date(2026, 9, 1),
      duration_minutes=45,
      notes="Morning upper body routine",
  )
  workout2 = Workout(
      date=date(2026, 9, 3), duration_minutes=30, notes="Cardio session"
  )

  db.session.add_all([workout1, workout2])
  db.session.commit()

  print("Linking exercises to workouts...")
  we1 = WorkoutExercises(
      workout=workout1, exercise=pushup, reps=20, sets=3, duration_seconds=0
  )
  we2 = WorkoutExercises(
      workout=workout1, exercise=squat, reps=15, sets=4, duration_seconds=0
  )
  we3 = WorkoutExercises(
      workout=workout2, exercise=running, reps=0, sets=0, duration_seconds=1800
  )

  db.session.add_all([we1, we2, we3])
  db.session.commit()

  print("🌱 Database seeded successfully!")