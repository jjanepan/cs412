"""
File: urls.py
Author: Jane Pan (jjanepan@bu.edu)
Description: This file defines the URL patterns for the Mini Facebook application.
             It maps URLs to their corresponding views, allowing users to view 
             all profiles, view individual profile pages, and create new profiles.
"""

from django.urls import path
from .views import (
    ShowAllProfilesView,
    ShowProfilePageView,
    CreateProfileView,
    CreateStatusMessageView
)

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),

    # New URL pattern for creating a status message
    path('profile/<int:pk>/create_status/', CreateStatusMessageView.as_view(), name='create_status'),
]
