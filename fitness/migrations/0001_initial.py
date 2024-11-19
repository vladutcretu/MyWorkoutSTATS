# Generated by Django 5.1 on 2024-11-18 16:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="MuscleGroup",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=30)),
                ("created", models.DateField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Exercise",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=30)),
                ("created", models.DateField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "musclegroup",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="fitness.musclegroup",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Workout",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=30)),
                ("bodyweight", models.FloatField(blank=True, null=True)),
                ("note", models.TextField(blank=True, max_length=100, null=True)),
                (
                    "public",
                    models.CharField(
                        choices=[("yes", "Yes"), ("no", "No")],
                        default="no",
                        max_length=3,
                    ),
                ),
                ("updated", models.DateField(auto_now=True)),
                ("created", models.DateField(blank=True, null=True)),
                (
                    "likes",
                    models.ManyToManyField(
                        blank=True,
                        related_name="workout_likes",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-created"],
            },
        ),
        migrations.CreateModel(
            name="WorkingSet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("warmup", "Warm Up set"),
                            ("working", "Working set"),
                            ("dropset", "Drop set"),
                            ("restpause", "Rest pause set"),
                            ("myo", "Myo set"),
                            ("cluster", "Cluster set"),
                            ("super", "Super set"),
                        ],
                        default="working",
                        max_length=10,
                    ),
                ),
                ("weight", models.FloatField(blank=True, null=True)),
                ("repetitions", models.IntegerField(blank=True, null=True)),
                ("distance", models.IntegerField(blank=True, null=True)),
                ("time", models.FloatField(blank=True, null=True)),
                ("updated", models.DateField(auto_now=True)),
                ("created", models.DateField(blank=True, null=True)),
                (
                    "exercise",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="workingsets",
                        to="fitness.exercise",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "workout",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="fitness.workout",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="WorkoutComment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField()),
                ("updated", models.DateTimeField(auto_now=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="replies",
                        to="fitness.workoutcomment",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "workout",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="fitness.workout",
                    ),
                ),
            ],
            options={
                "ordering": ["created"],
            },
        ),
        migrations.CreateModel(
            name="WorkoutExercise",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("order", models.PositiveIntegerField()),
                (
                    "exercise",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="fitness.exercise",
                    ),
                ),
                (
                    "workout",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="fitness.workout",
                    ),
                ),
            ],
            options={
                "ordering": ["workout"],
            },
        ),
        migrations.AddField(
            model_name="workout",
            name="exercises",
            field=models.ManyToManyField(
                blank=True,
                related_name="workouts",
                through="fitness.WorkoutExercise",
                to="fitness.exercise",
            ),
        ),
    ]
