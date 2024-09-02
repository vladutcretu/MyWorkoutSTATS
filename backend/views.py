from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User

from .forms import CustomUserRegistrationForm, AccountRecoveryForm


def main(request):
   """View for Main page"""
   return render (request, 'backend/main.html')


def user_login(request):
   """View for Log In page"""
   if request.user.is_authenticated:
      return redirect('main')
   
   if request.method == 'POST':
      username = request.POST.get('username').lower()
      password = request.POST.get('password')

      try: 
         user = User.objects.get(username=username)
      except:
         messages.error(request, "User does not exist")

      user = authenticate(request, username=username, password=password)

      if user is not None:
         login(request, user)
         return redirect('main')
      else:
         messages.error(request, "Password is incorrect")

   return render(request, 'backend/user_login.html')


def user_logout(request):
   """View for Log out page"""
   logout(request)
   return redirect('main')


def user_signup(request):
   """View for Sign Up page""" 
   if request.user.is_authenticated:
      return redirect('main')

   form = CustomUserRegistrationForm()

   if request.method == 'POST':
      form = CustomUserRegistrationForm(request.POST)
      if form.is_valid():
         user = form.save(commit=False)
         user.username = user.username.lower()
         user.save()
         login(request, user)
         return redirect('main')
      else:
         messages.error(request, "Something bad happened. Try again please!")

   context = {
      'form': form
   }
   return render (request, 'backend/user_signup.html', context)

def user_account_recovery(request):
   if request.user.is_authenticated:
      return redirect('main')
   
   form = AccountRecoveryForm()
   
   if request.method == 'POST':
      form = AccountRecoveryForm(request.POST)
      if form.is_valid():
         # Instructions to send recovery email here # 
         messages.success(request, 'An email has been sent to your email address with further instructions. Please check it!')
   else:
      form = AccountRecoveryForm()
   
   context = {
      'form' : form
   }
   return render(request, 'backend/user_recover.html', context)