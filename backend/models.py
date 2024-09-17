from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Model Custom for User to achieve profile feature"""
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(null=True, default='default.jpg')
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(max_length=300, blank=True, null=True)
    instagram_url = models.URLField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username
    

class MuscleGroup(models.Model):
    """Model for Muscle Groups"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Owner: {self.user} - Muscle Group: {self.name}"
    

class Exercise(models.Model):
    """Model For Exercises"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    musclegroup = models.ForeignKey(MuscleGroup, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.musclegroup} - Exercise: {self.name}"
    

class Workout(models.Model):
    """Model for Workouts"""
    PUBLIC_CHOICES = [
        ("yes", "Yes"),
        ("no", "No")
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    exercises = models.ManyToManyField(Exercise, through='WorkoutExercise', related_name='workouts', blank=True)
    bodyweight = models.FloatField(null=True, blank=True)
    note = models.TextField(max_length=100, null=True, blank=True)
    public = models.CharField(max_length=3, choices=PUBLIC_CHOICES, default="no")
    likes = models.ManyToManyField(CustomUser, related_name='workout_likes', blank=True)
    updated = models.DateField(auto_now=True)
    created = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"Owner: {self.user} - Workout: {self.name} - Date: {self.created}"

    def total_likes(self):
        return self.likes.count()
    

class WorkoutExercise(models.Model):
    """Model to assign an exercise to a specific workout"""
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['workout']
    
    def __str__(self):
        return f"Exercise #{self.order} - {self.workout}"
    

class WorkingSet(models.Model):
    """Model for Working Sets"""
    TYPE_CHOICES = [
        ("warmpup", "Warm Up set"),
        ("working", "Working set"),
        ("dropset", "Drop set"),
        ("restpause", "Rest pause set"),
        ("myo", "Myo set"),
        ("cluster", "Cluster set"),
        ("super", "Super set")
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, null=True, blank=True)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='workingsets')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default="working")
    weight = models.FloatField(null=True, blank=True)
    repetitions = models.IntegerField(null=True, blank=True)
    distance = models.IntegerField(null=True, blank=True)
    time = models.FloatField(null=True, blank=True)
    updated = models.DateField(auto_now=True)
    created = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.exercise} - Set: {self.weight} weight, {self.repetitions} reps | {self.distance} meters, {self.time} minutes"
    

class WorkoutComment(models.Model):
    """Model for comments section on public workouts, allowing replies to other comments."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f"{self.workout} - {self.user.username}: {self.content[:30]}..."
    
    @property
    def is_reply(self):
        """Checking if a comment is a reply"""
        return self.parent is not None