from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse
from .forms import CreateProfileForm, CreateStatusMessageForm
from .models import Profile, StatusMessage

class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'show_all_profiles.html'
    context_object_name = 'profiles'


class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'show_profile.html'
    # By default, the context object name is "object" (or "profile" if you set context_object_name).


class CreateProfileView(CreateView):
    """
    A view to create a new Profile.
    """
    form_class = CreateProfileForm
    template_name = 'create_profile_form.html'
    # By default, CreateView will call form.save() and then redirect
    # to the object's get_absolute_url method in the Profile model.


class CreateStatusMessageView(CreateView):
    """
    A view to create a new StatusMessage, attaching it to the correct Profile.
    """
    form_class = CreateStatusMessageForm
    template_name = 'create_status_form.html'  # Must match the file name in mini_fb/templates

    def get_context_data(self, **kwargs):
        """
        Include the Profile object in the template context
        so we can display the user's name or other details.
        """
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']              # The profile's primary key from the URL
        profile = Profile.objects.get(pk=pk)
        context['profile'] = profile
        return context

    def form_valid(self, form):
        """
        Attach the Profile to this new StatusMessage before saving.
        """
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        status_message = form.save(commit=False)
        status_message.profile = profile  # link the foreign key
        status_message.save()

        return super().form_valid(form)

    def get_success_url(self):
        """
        After creating the StatusMessage, redirect back to the same profile's page.
        """
        pk = self.kwargs['pk']
        return reverse('show_profile', kwargs={'pk': pk})
