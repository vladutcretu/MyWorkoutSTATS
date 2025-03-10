# Django
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

# App
from fitness.models import CustomUser, Workout
from core.forms import EditProfileForm


@login_required(login_url="login")
@cache_page(60 * 1440)  # one day
def user_account(request):
    """
    View for User Account page
    """
    return render(request, "user/account.html")


@login_required(login_url="login")
def user_profile(request, user_id):
    """
    View for User Profile page
    """
    user = CustomUser.objects.get(pk=user_id)
    public_workouts = Workout.objects.filter(user=user_id, public="yes")

    context = {"user": user, "public_workouts": public_workouts}
    return render(request, "user/profile.html", context)


@login_required(login_url="login")
def user_profile_edit(request):
    """
    View to edit user profile informations
    """
    if request.method == "POST":
        form = EditProfileForm(
            request.POST, request.FILES, instance=request.user
        )
        if form.is_valid():
            form.save()
            return redirect("profile", user_id=request.user.id)
    else:
        form = EditProfileForm(instance=request.user)

    context = {"form": form}
    return render(request, "user/edit_profile.html", context)
