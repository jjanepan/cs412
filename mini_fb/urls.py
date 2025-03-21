"""
File: urls.py
Author: Jane Pan (jjanepan@bu.edu)
Description: This file defines the URL patterns for the Mini Facebook application.
             It maps URLs to their corresponding views, allowing users to view 
             all profiles, view individual profile pages, create new profiles,
             manage status messages, view news feeds, and handle friend operations.
"""

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    ShowAllProfilesView,
    ShowProfilePageView,
    CreateProfileView,
    CreateStatusMessageView,
    UpdateProfileView,
    UpdateStatusMessageView,
    DeleteStatusMessageView,
    ShowNewsFeedView,
    ShowFriendSuggestionsView,
    AddFriendView
)

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    
    # URL pattern for creating a status message
    path('profile/<int:pk>/create_status/', CreateStatusMessageView.as_view(), name='create_status'),
    
    # URL pattern for updating a profile
    path('profile/<int:pk>/update/', UpdateProfileView.as_view(), name='update_profile'),
    
    # URL pattern for updating a status message
    path('status/<int:pk>/update/', UpdateStatusMessageView.as_view(), name='update_status'),
    
    # URL pattern for deleting a status message
    path('status/<int:pk>/delete/', DeleteStatusMessageView.as_view(), name='delete_status'),

    # URL pattern for displaying the news feed for a profile
    path('profile/<int:pk>/news_feed/', ShowNewsFeedView.as_view(), name='news_feed'),

    # URL pattern for showing friend suggestions for a profile
    path('profile/<int:pk>/friend_suggestions/', ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
    
    # URL pattern for adding a friend (pk = current profile, other_pk = profile to add)
    path('profile/<int:pk>/add_friend/<int:other_pk>/', AddFriendView.as_view(), name='add_friend'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
