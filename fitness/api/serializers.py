# Django & DRF
from rest_framework import serializers

# App
from fitness.models import MuscleGroup, Exercise, Workout, WorkingSet


class MuscleGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MuscleGroup
        fields = ['id', 'name', 'created']


class ExerciseSerializer(serializers.ModelSerializer):
    musclegroup = serializers.CharField(write_only=True) # Accept musclegroup name in POST
    musclegroup_details = MuscleGroupSerializer(read_only=True, source='musclegroup')  # Return full musclegroup details in GET

    class Meta:
        model = Exercise
        fields = ['id', 'name', 'musclegroup', 'musclegroup_details', 'created']

    def validate_musclegroup(self, value):
        """Check if user introduced a valid (existing and owned) muscle group."""
        user = self.context['request'].user
        try:
            return MuscleGroup.objects.get(name=value, user=user)
        except MuscleGroup.DoesNotExist:
            raise serializers.ValidationError("User does not have the specified muscle group. Try create it or specify an existing one!")


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['id', 'name', 'exercises', 'public', 'updated', 'created']
    
    def validate(self, attrs):
        """Check if the user already has a workout for the specified date."""
        user = self.context['request'].user
        created_date = attrs.get('created')

        # Check if request is POST or PUT/PATCH
        if self.instance:
            # PUT/PATCH request
            existing_workouts = Workout.objects.filter(user=user, created=created_date).exclude(id=self.instance.id)
        else:
            # POST request
            existing_workouts = Workout.objects.filter(user=user, created=created_date)

        if existing_workouts.exists():
            raise serializers.ValidationError({"created": "You already have a workout created for this date. Try another date or delete the existing workout!"})
        return attrs
    

class WorkingSetSerializer(serializers.ModelSerializer):
    workout = serializers.IntegerField(write_only=True) # Accept workout id in POST
    exercise = serializers.IntegerField(write_only=True) # Accept exercise id in POST
    workout_details = MuscleGroupSerializer(read_only=True, source='workout')  # Return full workout details in GET
    exercise_details = MuscleGroupSerializer(read_only=True, source='exercise')  # Return full exercise details in GET

    class Meta:
        model = WorkingSet
        fields = ['id', 'workout', 'workout_details', 'exercise', 'exercise_details', 'type', 'weight', 'repetitions', 'distance', 'time', 'updated', 'created']

    def validate(self, attrs):
        """Check if the workout and exercise are related and valid (existing and owned by requested user)."""
        user = self.context['request'].user
        workout_id = attrs.get('workout')
        exercise_id = attrs.get('exercise')

        # Check if workout ID exists and is owned by requested user
        try:
            workout = Workout.objects.get(id=workout_id, user=user)
        except Workout.DoesNotExist:
            raise serializers.ValidationError({"workout": "User does not have the specified workout. Please specify an existing workout ID!"})

        # Check if the exercise ID exists and is owned by requested user
        try:
            exercise = Exercise.objects.get(id=exercise_id, user=user)
        except Exercise.DoesNotExist:
            raise serializers.ValidationError({"exercise": "User does not have the specified exercise. Please specify an existing exercise ID!"})

        # Check if workout and exercise is related (exercise is added to the workout)
        if not workout.exercises.filter(id=exercise_id).exists():
            raise serializers.ValidationError({"exercise": "The specified exercise is not associated with the specified workout. Please add exercise to the workout first!"})

        attrs['workout'] = workout
        attrs['exercise'] = exercise
        return attrs