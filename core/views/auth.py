# Django
from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    update_session_auth_hash,
)
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# App
from core.models import CustomUser
from core.forms import (
    CustomUserRegistrationForm,
    AccountRecoveryForm,
    ChangePasswordForm,
)


def user_login(request):
    """
    View for Log In page
    """
    if request.user.is_authenticated:
        return redirect("main")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            messages.error(request, "User does not exist")

        if username and password:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("main")
            else:
                messages.error(request, "Password is incorrect")

    return render(request, "auth/login.html")


def user_logout(request):
    """
    View for Log out page
    """
    logout(request)
    return redirect("main")


def user_signup(request):
    """
    View for Sign Up page
    """
    if request.user.is_authenticated:
        return redirect("main")

    form = CustomUserRegistrationForm()

    if request.method == "POST":
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("main")
        else:
            messages.error(
                request, "Something bad happened. Try again please!"
            )

    context = {"form": form}
    return render(request, "auth/signup.html", context)


def user_account_recovery(request):
    """
    View for User Account Recovery page
    """
    if request.user.is_authenticated:
        return redirect("main")

    form = AccountRecoveryForm()

    if request.method == "POST":
        form = AccountRecoveryForm(request.POST)
        if form.is_valid():
            # Instructions to send recovery email here
            messages.success(
                request,
                "An email has been sent to your email address with further"
                "instructions. Please check it!",
            )
    else:
        form = AccountRecoveryForm()

    context = {"form": form}
    return render(request, "auth/recover.html", context)


@login_required(login_url="login")
def user_change_password(request):
    """
    View for Change Password page
    """
    if request.method == "POST":
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password has been changed.")
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = ChangePasswordForm(request.user)

    context = {"form": form}
    return render(request, "auth/change_password.html", context)


@login_required(login_url="login")
def user_delete_account(request):
    """
    View used by an user to delete his account
    """
    user = request.user

    if request.method == "POST":
        user.delete()
        return redirect("main")

    context = {"user": user}

    return render(request, "auth/delete_account.html", context)
