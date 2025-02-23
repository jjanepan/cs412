# views.py - Views for the Profiles App
# This file defines class-based views (CBVs) for displaying profile-related information.

from django.views.generic import ListView, DetailView  # Import generic class-based views
from .models import Profile  # Import the Profile model

# View to display a list of all profiles
class ShowAllProfilesView(ListView):
    model = Profile  # Specifies the model to query
    template_name = 'show_all_profiles.html'  # Template used to render the view
    context_object_name = 'profiles'  # Custom name for the context variable passed to the template

# View to display the details of a single profile
class ShowProfilePageView(DetailView):
    model = Profile  # Specifies the model to query
    template_name = 'show_profile.html'  # Template used to render the view
    # By default, Django sets the context object name to "object" or the model name in lowercase ("profile" in this case)
