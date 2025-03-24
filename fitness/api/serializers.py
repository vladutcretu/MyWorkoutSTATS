# Django & DRF
from rest_framework import serializers

# App
from fitness.models import (
    MuscleGroup,
    Exercise,
    Workout,
    WorkoutExercise,
    WorkingSet,
)


class MuscleGroupSerializer(serializers.ModelSerializer):
    """
    Serializer for MuscleGroup API View
    """

    class Meta:
        model = MuscleGroup
        fields = ["id", "name", "created"]


class ExerciseSerializer(serializers.ModelSerializer):
    """
    Serializer for Exercise API View
    """

    musclegroup_id = serializers.IntegerField(
        write_only=True
    )  # Accept musclegroup name in POST
    musclegroup_details = MuscleGroupSerializer(
        read_only=True, source="musclegroup"
    )  # Return full musclegroup details in GET

    class Meta:
        model = Exercise
        fields = [
            "id",
            "name",
            "musclegroup_id",
            "musclegroup_details",
            "created",
        ]

    def validate(self, attrs):
        """
        Check if user introduced a valid (existing and owned) muscle group.
        """
        user = self.context["request"].user
        musclegroup_id = attrs.get("musclegroup_id")

        # Check if musclegroup ID exists and is owned by requested user
        try:
            musclegroup = MuscleGroup.objects.get(id=musclegroup_id, user=user)
        except MuscleGroup.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "musclegroup_id": (
                        "User does not have the specified muscle group. "
                        "Please specify an existing muscle group ID!"
                    )
                }
            )

        attrs["musclegroup"] = musclegroup
        return attrs


class WorkoutSerializer(serializers.ModelSerializer):
    """
    Serializer for Workout API View
    """

    class Meta:
        model = Workout
        fields = [
            "id",
            "name",
            "bodyweight",
            "note",
            "public",
            "updated",
            "created",
        ]

    def get_fields(self):
        """
        Hide`created` field on PUT/PATCH methods, but show it on POST method.
        """
        fields = super().get_fields()
        request = self.context.get("request", None)

        if request and request.method in ["PUT", "PATCH"]:
            fields.pop("created", None)
        return fields

    def validate(self, attrs):
        """Check if the user already has a workout for the specified date."""
        user = self.context["request"].user
        created_date = attrs.get("created")

        # Check if request is POST or PUT/PATCH
        if self.instance:
            # PUT/PATCH request
            existing_workouts = Workout.objects.filter(
                user=user, created=created_date
            ).exclude(id=self.instance.id)
        else:
            # POST request
            existing_workouts = Workout.objects.filter(
                user=user, created=created_date
            )

        if existing_workouts.exists():
            raise serializers.ValidationError(
                {
                    "workout": (
                        "You already have a workout created for this date. "
                        "Try another date or delete the existing workout!"
                    )
                }
            )
        return attrs


class WorkoutExerciseSerializer(serializers.ModelSerializer):
    """
    Serializer for WorkoutExercise API View
    """

    workout_id = serializers.IntegerField(
        write_only=True
    )  # Accept workout id in POST
    exercise_id = serializers.IntegerField(
        write_only=True
    )  # Accept exercise id in POST
    workout_details = WorkoutSerializer(
        read_only=True, source="workout"
    )  # Return full workout details in GET
    exercise_details = ExerciseSerializer(
        read_only=True, source="exercise"
    )  # Return full exercise details in GET
    order = serializers.IntegerField(
        read_only=True
    )  # order is automaticaly calculated

    class Meta:
        model = WorkoutExercise
        fields = [
            "id",
            "workout_id",
            "exercise_id",
            "workout_details",
            "exercise_details",
            "order",
        ]

    def validate(self, attrs):
        """
        Check if the workout and exercise are valid,
        existing and owned by requested user.
        """
        user = self.context["request"].user

        # Check if workout ID exists and is owned by requested user
        try:
            workout = Workout.objects.get(id=attrs["workout_id"], user=user)
        except Workout.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "workout_id": (
                        "User does not have the specified workout. "
                        "Please specify an existing workout ID!"
                    )
                }
            )

        # Check if the exercise ID exists and is owned by requested user
        try:
            exercise = Exercise.objects.get(id=attrs["exercise_id"], user=user)
        except Exercise.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "exercise_id": (
                        "User does not have the specified exercise."
                        " Please specify an existing exercise ID!"
                    )
                }
            )

        # Check if workout and exercise are already related
        if WorkoutExercise.objects.filter(
            workout=workout, exercise=exercise
        ).exists():
            raise serializers.ValidationError(
                {
                    "exercise_id": (
                        "The specified exercise is already associated "
                        "with the specified workout!"
                    )
                }
            )

        attrs["workout"] = workout
        attrs["exercise"] = exercise
        return attrs

    def create(self, validated_data):
        """
        Create workout - exercise relationship
        """
        # Delete not needed fields
        validated_data.pop("workout_id")
        validated_data.pop("exercise_id")
        return super().create(validated_data)


class WorkingSetSerializer(serializers.ModelSerializer):
    """
    Serializer for WorkingSet API View
    """

    workout_exercise_id = serializers.IntegerField(
        write_only=True
    )  # Accept workout_exercise id in POST
    workout_exercise_details = WorkoutExerciseSerializer(
        read_only=True, source="workout_exercise"
    )  # Return full workout_exercise details in GET

    class Meta:
        model = WorkingSet
        fields = [
            "id",
            "workout_exercise_id",
            "workout_exercise_details",
            "type",
            "weight",
            "repetitions",
            "distance",
            "time",
            "updated",
            "created",
        ]

    def validate(self, attrs):
        """
        Check if the workout_exercise exists and is owned by requested user
        """
        user = self.context["request"].user
        workout_exercise_id = attrs.get("workout_exercise_id")

        # Check if workout_exercise ID exists and is owned by requested user
        try:
            workout_exercise = WorkoutExercise.objects.get(
                id=workout_exercise_id, user=user
            )
        except WorkoutExercise.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "workout": (
                        "User does not have the specified workout. "
                        "Please specify an existing workout ID!"
                    )
                }
            )

        attrs["workout_exercise"] = workout_exercise
        return attrs


class DetailedWorkingSetSerializer(serializers.ModelSerializer):
    """
    Detailed version of working set serializer to use it for
    Detailed workout serializer.
    """

    class Meta:
        model = WorkingSet
        fields = ["id", "type", "weight", "repetitions", "distance", "time"]


class DetailedExerciseSerializer(serializers.ModelSerializer):
    """
    Detailed version of exercise serializer to use it for Detailed workout
    serializer.
    """

    name = serializers.CharField(source="exercise.name", read_only=True)
    sets = serializers.SerializerMethodField()

    class Meta:
        model = WorkoutExercise
        fields = ["id", "name", "sets"]

    def get_sets(self, obj):
        """
        Get all sets associated with this exercise within the specific workout.
        """
        workout_id = self.context.get("workout_id")
        sets = WorkingSet.objects.filter(
            workout_id=workout_id, exercise=obj.exercise
        )  # Get sets based on the exercise
        return DetailedWorkingSetSerializer(sets, many=True).data


class DetailedWorkoutSerializer(serializers.ModelSerializer):
    """
    Detailed version of workout serializer to use it for
    Detailed workout API view.
    """

    exercises = serializers.SerializerMethodField()

    class Meta:
        model = Workout
        fields = [
            "id",
            "name",
            "created",
            "updated",
            "bodyweight",
            "note",
            "public",
            "exercises",
        ]

    def get_exercises(self, obj):
        """
        Get all exercises associated with this workout, alongside with their
        sets.
        """
        workout_exercises = (
            WorkoutExercise.objects.filter(workout=obj)
            .select_related("exercise")
            .prefetch_related("workingsets")
        )  # Optimized filter with select_related
        # serializer = DetailedExerciseSerializer(
        #     workout_exercises, many=True, context={"workout_id": obj.id}
        # )
        # return serializer.data

        # Create a custom data structure for the response
        exercises_data = []
        for we in workout_exercises:
            exercise_data = {
                "sets": WorkingSetSerializer(
                    we.workingsets.all(), many=True
                ).data
            }
            exercises_data.append(exercise_data)

        return exercises_data
