from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class MuscleGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Owner: {self.user} - Muscle Group: {self.name}"
    

class Exercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    musclegroup = models.ForeignKey(MuscleGroup, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.musclegroup} - Exercise: {self.name}"


class Workout(models.Model):
    PUBLIC_CHOICES = [
        ("yes", "Yes"),
        ("no", "No"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    exercises = models.ManyToManyField(Exercise, through='WorkoutExercise', related_name='workouts', blank=True)
    bodyweight = models.FloatField(null=True, blank=True)
    public = models.CharField(max_length=3, choices=PUBLIC_CHOICES, default="no")
    note = models.TextField(max_length=100, null=True, blank=True)
    updated = models.DateField(auto_now=True)
    created = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"Owner: {self.user} - Workout: {self.name} - Date: {self.created} - Visibilty: {self.public}"
    

class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"Exercise #{self.order} for {self.workout}"


class WorkingSet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, null=True, blank=True)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='workingsets')
    weight = models.FloatField(null=True, blank=True)
    repetitions = models.IntegerField(null=True, blank=True)
    distance = models.IntegerField(null=True, blank=True)
    time = models.FloatField(null=True, blank=True)
    updated = models.DateField(auto_now=True)
    created = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.exercise} - Set: {self.weight} weight, {self.repetitions} reps | {self.distance} meters, {self.time} minutes"