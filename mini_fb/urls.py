# urls.py - URL Configuration for the Profiles App
# This file defines URL patterns that map to views for handling profile-related requests.

from django.urls import path  # Import Django's path function for URL routing
from .views import ShowAllProfilesView, ShowProfilePageView  # Import the views

urlpatterns = [
    # Route to display all profiles
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),

    # Route to display a specific profile by its primary key (pk)
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile'),
]
