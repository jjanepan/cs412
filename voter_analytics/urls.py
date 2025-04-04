"""
Author: Jane Pan (jjanepan@bu.edu)
Description: URL patterns for the Voter Analytics application.
             It maps URLs to views for listing voters, showing voter details,
             and displaying graphs of voter data.
"""

from django.urls import path
from .views import (
    VoterListView, 
    VoterDetailView,
    VoterGraphsView
)

urlpatterns = [
    # URL pattern for listing all voters (paginated)
    path('', VoterListView.as_view(), name='voters'),
    
    # URL pattern for viewing details of a single voter
    path('voter/<int:pk>/', VoterDetailView.as_view(), name='voter'),
    
    # URL pattern for displaying graphs (all three graphs on one page)
    path('graphs/', VoterGraphsView.as_view(), name='graphs'),
]
