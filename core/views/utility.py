# Django
from django.shortcuts import render
from django.views.decorators.cache import cache_page


@cache_page(60 * 1440)  # one day
def page_about(request):
    """
    View for About page
    """
    return render(request, "utility/about.html")


@cache_page(60 * 1440)  # one day
def page_rest_api(request):
    """
    View for REST API presentation page
    """
    return render(request, "utility/rest_api.html")


@cache_page(60 * 1440)  # one day
def page_help(request):
    """
    View for Help page
    """
    return render(request, "utility/help.html")


@cache_page(60 * 1440)  # one day
def page_privacy(request):
    """
    View for Privacy & Terms page
    """
    return render(request, "utility/privacy.html")
