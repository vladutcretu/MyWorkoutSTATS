# Django & DRF
from rest_framework import serializers

# App
from fitness.models import MuscleGroup

class MuscleGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MuscleGroup
        fields = ['id', 'name', 'created']

