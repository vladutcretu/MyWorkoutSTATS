# Django & DRF
from rest_framework import serializers

# App
from fitness.models import MuscleGroup, Exercise


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

