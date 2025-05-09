# Django
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.cache import cache

# App
from fitness.models import MuscleGroup
from fitness.forms import MuscleGroupForm


@login_required(login_url="login")
def view_musclegroups(request):
    """
    View used by user to see all muscle groups
    """
    # Get musclegroups from cache (if exists) or from database
    cache_key_musclegroups = f"view_musclegroups_{request.user.id}"
    musclegroups = cache.get(cache_key_musclegroups)
    if not musclegroups:
        musclegroups = MuscleGroup.objects.filter(user=request.user)
        cache.set(cache_key_musclegroups, musclegroups, timeout=60 * 60)

    musclegroups_count = len(musclegroups)

    context = {
        "musclegroups": musclegroups,
        "musclegroups_count": musclegroups_count,
    }
    return render(request, "musclegroups/view.html", context)


@login_required(login_url="login")
def create_musclegroups(request):
    """
    View used by user to add a muscle group
    """
    if request.method == "POST":
        form = MuscleGroupForm(request.POST)
        if form.is_valid():
            musclegroup = form.save(commit=False)
            musclegroup.user = request.user
            musclegroup.save()

            # Once create a musclegroup invalidate musclegroup cache
            cache_key_musclegroups = f"view_musclegroups_{request.user.id}"
            cache.delete(cache_key_musclegroups)

            return redirect("musclegroups")
    else:
        form = MuscleGroupForm()

    context = {"form": form}
    return render(request, "musclegroups/create.html", context)


@login_required(login_url="login")
def edit_musclegroups(request, musclegroup_id):
    """
    View used to edit fields from existing muscle group
    """
    musclegroup = get_object_or_404(
        MuscleGroup, pk=musclegroup_id, user=request.user
    )
    form = MuscleGroupForm(instance=musclegroup)

    if request.method == "POST":
        form = MuscleGroupForm(request.POST, instance=musclegroup)
        if form.is_valid():
            form.save()

            # Once edit a musclegroup invalidate musclegroup cache
            cache_key_musclegroups = f"view_musclegroups_{request.user.id}"
            cache.delete(cache_key_musclegroups)

            return redirect("musclegroups")

    context = {"form": form}
    return render(request, "musclegroups/create.html", context)


@login_required(login_url="login")
def delete_musclegroups(request, musclegroup_id):
    """
    View used by user to delete muscle group
    """
    musclegroup = get_object_or_404(
        MuscleGroup, pk=musclegroup_id, user=request.user
    )

    if request.method == "POST":
        musclegroup.delete()

        # Once delete a musclegroup invalidate musclegroup cache
        cache_key_musclegroups = f"view_musclegroups_{request.user.id}"
        cache.delete(cache_key_musclegroups)

        return redirect("musclegroups")

    context = {"musclegroup": musclegroup}
    return render(request, "musclegroups/delete.html", context)
