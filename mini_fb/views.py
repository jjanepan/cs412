from django.views.generic import ListView
from django.views.generic import DetailView

from .models import Profile
class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'show_all_profiles.html'
    context_object_name = 'profiles'
class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'show_profile.html'
    # By default, the context object name is "object" or "profile" depending on the model
