# Django & DRF
from rest_framework import serializers

# App
from fitness.models import MuscleGroup, Exercise, Workout


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
        fields = ['id', 'name', 'public', 'updated', 'created']
    
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