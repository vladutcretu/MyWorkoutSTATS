# Django
from django.urls import path

# App
from core.views import (
    auth,
    main,
    user,
    utility
)


urlpatterns = [
    # Main page urls
    path('', main.main, name='main'),

    # Utility urls
    path('about/', utility.page_about, name='about'),
    path('rest-api/', utility.page_rest_api, name='rest-api'),
    path('help/', utility.page_help, name='help'),
    path('privacy/', utility.page_privacy, name='privacy'),

    # Auth urls
    path('login/', auth.user_login, name='login'),
    path('logout/', auth.user_logout, name='logout'),
    path('signup/', auth.user_signup, name='signup'),
    path('recover/', auth.user_account_recovery, name='recover'),
    path('change-password/', auth.user_change_password, name='change-password'),
    path('delete-account/', auth.user_delete_account, name='delete-account'),

    # User profile and account urls
    path('account/', user.user_account, name='account'),
    path('profile/<int:user_id>/', user.user_profile, name='profile'),
    path('profile/edit-profile/', user.user_profile_edit, name='edit-profile'),
]