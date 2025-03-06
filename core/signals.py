# Django
from django.db.models.signals import post_save
from django.dispatch import receiver

# App
from core.models import CustomUser
from fitness.models import MuscleGroup, Exercise


@receiver(post_save, sender=CustomUser)
def create_user_account(sender, instance, created, **kwargs):
    """
    Method to create by default muscle groups and related exercises for
    each new user registered
    """
    if created:
        # Create Muscle Groups
        musclegroup_abs = MuscleGroup.objects.create(user=instance, name="Abs")
        musclegroup_back = MuscleGroup.objects.create(
            user=instance, name="Back"
        )
        musclegroup_biceps = MuscleGroup.objects.create(
            user=instance, name="Biceps"
        )
        musclegroup_cardio = MuscleGroup.objects.create(
            user=instance, name="Cardio"
        )
        musclegroup_chest = MuscleGroup.objects.create(
            user=instance, name="Chest"
        )
        musclegroup_legs = MuscleGroup.objects.create(
            user=instance, name="Legs"
        )
        musclegroup_shoulders = MuscleGroup.objects.create(
            user=instance, name="Shoulders"
        )
        musclegroup_triceps = MuscleGroup.objects.create(
            user=instance, name="Triceps"
        )

        # Create Exercises for Abs (ID 1)
        Exercise.objects.create(
            user=instance, musclegroup=musclegroup_abs, name="Ab Wheel Rollout"
        )
        Exercise.objects.create(
            user=instance, musclegroup=musclegroup_abs, name="Crunch"
        )
        Exercise.objects.create(
            user=instance, musclegroup=musclegroup_abs, name="Crunch (Cable)"
        )
        Exercise.objects.create(
            user=instance, musclegroup=musclegroup_abs, name="Crunch (Machine)"
        )
        Exercise.objects.create(
            user=instance, musclegroup=musclegroup_abs, name="Decline Crunch"
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_abs,
            name="Hanging Knee Raise",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_abs,
            name="Hanging Leg Raise",
        )
        Exercise.objects.create(
            user=instance, musclegroup=musclegroup_abs, name="Russian Twist"
        )
        Exercise.objects.create(
            user=instance, musclegroup=musclegroup_abs, name="Plank"
        )
        Exercise.objects.create(
            user=instance, musclegroup=musclegroup_abs, name="Side Plank"
        )

        # Create Exercises for Back (ID 2)
        Exercise.objects.create(
            user=instance, musclegroup=musclegroup_back, name="Back Extension"
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_back,
            name="Bent Over Row - One Arm (Dumbell)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_back,
            name="Bent Over Row (Barbell)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_back,
            name="Bent Over Row (Dumbell)",
        )
        Exercise.objects.create(
            user=instance, musclegroup=musclegroup_back, name="Chin Up"
        )
        Exercise.objects.create(
            user=instance, musclegroup=musclegroup_back, name="Deadlift"
        )
        Exercise.objects.create(
            user=instance, musclegroup=musclegroup_back, name="Good Morning"
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_back,
            name="Lat Pullover (Cable)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_back,
            name="Lat Pulldown (Cable)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_back,
            name="Lat Pulldown (Machine)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_back,
            name="Lat Pulldown (Single Arm)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_back,
            name="Pendlay Row (Barbell)",
        )
        Exercise.objects.create(
            user=instance, musclegroup=musclegroup_back, name="Pull Up"
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_back,
            name="Rack Pull (Barbell)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_back,
            name="Seated Row (Cable)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_back,
            name="Seated Row (Machine)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_back,
            name="Seated Row - wide grip (Cable)",
        )
        Exercise.objects.create(
            user=instance, musclegroup=musclegroup_back, name="Shrug (Barbell)"
        )
        Exercise.objects.create(
            user=instance, musclegroup=musclegroup_back, name="Shrug (Dumbell)"
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_back,
            name="Shrug (Smith Machine)",
        )
        Exercise.objects.create(
            user=instance, musclegroup=musclegroup_back, name="T-Bar Row"
        )

        # Create Exercises for Biceps (ID 3)
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_biceps,
            name="Bicep Curl (Barbell)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_biceps,
            name="Bicep Curl (Cable)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_biceps,
            name="Bicep Curl (Dumbell)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_biceps,
            name="Bicep Curl (Machine)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_biceps,
            name="Bicep Reverse Curl (Barbell)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_biceps,
            name="Concentration Curl (Dumbell)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_biceps,
            name="Hammer Curl (Cable)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_biceps,
            name="Hammer Curl (Dumbell)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_biceps,
            name="Preacher Curl (Barbell)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_biceps,
            name="Preacher Curl (Dumbell)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_biceps,
            name="Preacher Curl (Machine)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_biceps,
            name="Seated Incline Curl (Dumbell)",
        )
        Exercise.objects.create(
            user=instance, musclegroup=musclegroup_biceps, name="Wrist Roller"
        )

        # Create Exercises for Cardio (ID 4)
        Exercise.objects.create(
            user=instance, musclegroup=musclegroup_cardio, name="Battle Ropes"
        )
        Exercise.objects.create(
            user=instance, musclegroup=musclegroup_cardio, name="Boxing"
        )
        Exercise.objects.create(
            user=instance, musclegroup=musclegroup_cardio, name="Cycling"
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_cardio,
            name="Cycling (Indoor)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_cardio,
            name="Elliptical Machine",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_cardio,
            name="Rowing Machine",
        )
        Exercise.objects.create(
            user=instance, musclegroup=musclegroup_cardio, name="Running"
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_cardio,
            name="Running (Treadmill)",
        )
        Exercise.objects.create(
            user=instance, musclegroup=musclegroup_cardio, name="Swimming"
        )
        Exercise.objects.create(
            user=instance, musclegroup=musclegroup_cardio, name="Walking"
        )

        # Create Exercises for Chest (ID 5)
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_chest,
            name="Bench Press (Barbell)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_chest,
            name="Bench Press (Cable)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_chest,
            name="Bench Press (Dumbell)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_chest,
            name="Bench Press (Smith Machine)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_chest,
            name="Cable Crossover",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_chest,
            name="Cable Chest Fly (High)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_chest,
            name="Cable Chest Fly (Medium)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_chest,
            name="Cable Chest Fly (Low)",
        )
        Exercise.objects.create(
            user=instance, musclegroup=musclegroup_chest, name="Chest Dip"
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_chest,
            name="Chest Fly (Dumbell)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_chest,
            name="Chest Press (Machine)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_chest,
            name="Decline Bench Press (Barbell)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_chest,
            name="Decline Bench Press (Dumbell)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_chest,
            name="Decline Bench Press (Smith Machine)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_chest,
            name="Decline Chest Press (Machine)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_chest,
            name="Incline Bench Press (Barbell)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_chest,
            name="Incline Bench Press (Cable)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_chest,
            name="Incline Bench Press (Dumbell)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_chest,
            name="Incline Bench Press (Smith Machine)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_chest,
            name="Incline Chest Press (Machine)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_chest,
            name="Pec Deck (Machine)",
        )
        Exercise.objects.create(
            user=instance, musclegroup=musclegroup_chest, name="Push Up"
        )

        # Create Exercises for Legs (ID 6)
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_legs,
            name="Bulgarian Split Squat",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_legs,
            name="Calf Press (Machine)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_legs,
            name="Calf Raise (Barbell)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_legs,
            name="Calf Raise (Bodyweight)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_legs,
            name="Calf Raise (Dumbell)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_legs,
            name="Calf Raise (Smith Machine)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_legs,
            name="Calf Raise - Seated (Machine)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_legs,
            name="Front Squat (Barbell)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_legs,
            name="Hack Squat (Machine)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_legs,
            name="Hip Abductor (Machine)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_legs,
            name="Hip Thrust (Barbell)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_legs,
            name="Leg Extension (Machine)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_legs,
            name="Leg Press (Machine)",
        )
        Exercise.objects.create(
            user=instance, musclegroup=musclegroup_legs, name="Lunge (Barbell)"
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_legs,
            name="Lunge (Bodyweight)",
        )
        Exercise.objects.create(
            user=instance, musclegroup=musclegroup_legs, name="Lunge (Dumbell)"
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_legs,
            name="Leg Curl - Lying (Machine)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_legs,
            name="Leg Curl - Seated (Machine)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_legs,
            name="Romanian Deadlift (Barbell)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_legs,
            name="Romanian Deadlift (Dumbell)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_legs,
            name="Romanian Deadlift (Smith Machine)",
        )
        Exercise.objects.create(
            user=instance, musclegroup=musclegroup_legs, name="Squat (Barbell)"
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_legs,
            name="Squat (Bodyweight)",
        )
        Exercise.objects.create(
            user=instance, musclegroup=musclegroup_legs, name="Squat (Dumbell)"
        )
        Exercise.objects.create(
            user=instance, musclegroup=musclegroup_legs, name="Squat (Machine)"
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_legs,
            name="Squat (Smith Machine)",
        )
        Exercise.objects.create(
            user=instance, musclegroup=musclegroup_legs, name="Sumo Deadlift"
        )

        # Create Exercises for Shoulders (ID 7)
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_shoulders,
            name="Arnold Press (Dumbell)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_shoulders,
            name="Face Pull (Cable)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_shoulders,
            name="Front Raise (Dumbell)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_shoulders,
            name="Lateral Raise (Cable)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_shoulders,
            name="Lateral Raise (Dumbell)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_shoulders,
            name="Lateral Raise (Machine)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_shoulders,
            name="Overhead Press (Barbell)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_shoulders,
            name="Overhead Press (Dumbell)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_shoulders,
            name="Overhead Press (Smith Machine)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_shoulders,
            name="Reverse Fly (Cable)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_shoulders,
            name="Reverse Fly (Dumbell)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_shoulders,
            name="Reverse Fly (Machine)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_shoulders,
            name="Shoulder Press (Machine)",
        )

        # Create Exercises for Triceps (ID 8)
        Exercise.objects.create(
            user=instance, musclegroup=musclegroup_triceps, name="Bench Dip"
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_triceps,
            name="Bench Press - close grip (Barbell)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_triceps,
            name="Bench Press - close grip (Smith Machine)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_triceps,
            name="Push Down - cable cross",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_triceps,
            name="Push Down (Bar)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_triceps,
            name="Push Down (Rope)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_triceps,
            name="Push Down (V Bar)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_triceps,
            name="Skullcrusher (Barbell)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_triceps,
            name="Skullcrusher (Dumbell)",
        )
        Exercise.objects.create(
            user=instance, musclegroup=musclegroup_triceps, name="Tricep Dip"
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_triceps,
            name="Tricep Overhead Extension (Cable)",
        )
        Exercise.objects.create(
            user=instance,
            musclegroup=musclegroup_triceps,
            name="Tricep Overhead Extension (Dumbell)",
        )
