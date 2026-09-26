from marshmallow import Schema, fields, validate

class ExerciseSchema(Schema):
  id = fields.Int(dump_only=True)
  name = fields.Str(required=True, validate=validate.Length(min=1))
  category = fields.Str(validate=validate.OneOf(["Cardio", "Strength", "Flexibility", "Balance"],error="Category must be one of: Cardio, Strength, Flexibility, Balance",))
  equipment_needed = fields.Bool()

  # Exclude 'exercise' inside workout_exercises to prevent recursion
  workout_exercises = fields.Nested("WorkoutExercisesSchema", many=True, exclude=("exercise",))

class WorkoutSchema(Schema):
  id = fields.Int(dump_only=True)
  date = fields.Date(required=True)
  duration_minutes = fields.Int(validate=validate.Range(min=1, error="Duration must be at least 1 minute."))
  notes = fields.Str()

  # Exclude 'workout' inside workout_exercises to prevent recursion
  workout_exercises = fields.Nested("WorkoutExercisesSchema", many=True, exclude=("workout",))

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