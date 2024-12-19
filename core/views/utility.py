# Django
from django.shortcuts import render


def page_about(request):
   return render(request, 'utility/about.html')

def page_rest_api(request):
   return render(request, 'utility/rest_api.html')

def page_help(request):
   return render(request, 'utility/help.html')

def page_privacy(request):
   return render(request, 'utility/privacy.html')