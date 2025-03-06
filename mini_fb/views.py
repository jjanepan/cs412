"""
views.py

This module contains Django class-based views for handling Profile and StatusMessage operations,
including listing, creating, updating, and deleting profiles and status messages. It also supports
image uploads associated with status messages.

Views:
- ShowAllProfilesView: Displays a list of all profiles.
- ShowProfilePageView: Displays details of a single profile.
- CreateProfileView: Allows users to create a new profile.
- CreateStatusMessageView: Allows users to create a status message with image uploads.
- UpdateProfileView: Allows users to update an existing profile.
- UpdateStatusMessageView: Allows users to update a status message.
- DeleteStatusMessageView: Allows users to delete a status message with confirmation.

Dependencies:
- Django class-based views (ListView, DetailView, CreateView, UpdateView, DeleteView)
- Django's reverse function for URL redirection.
- Models: Profile, StatusMessage, Image, StatusImage
- Forms: CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusMessageForm

Author: [Your Name]
Date: [Current Date]
"""

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from .forms import (
    CreateProfileForm,
    CreateStatusMessageForm,
    UpdateProfileForm,
    UpdateStatusMessageForm
)
from .models import Profile, StatusMessage, Image, StatusImage

class ShowAllProfilesView(ListView):
    """
    Displays a list of all Profiles.
    """
    model = Profile
    template_name = 'show_all_profiles.html'
    context_object_name = 'profiles'  # Passes profiles list to the template

class ShowProfilePageView(DetailView):
    """
    Displays the details of a single Profile.
    """
    model = Profile
    template_name = 'show_profile.html'
    # The default context object is "object" referring to the Profile instance.

class CreateProfileView(CreateView):
    """
    A view to create a new Profile.
    Uses CreateProfileForm for input.
    After creation, it redirects to the profile's get_absolute_url.
    """
    form_class = CreateProfileForm
    template_name = 'create_profile_form.html'

class CreateStatusMessageView(CreateView):
    """
    A view to create a new StatusMessage and attach it to the correct Profile.
    This view also handles image uploads and associates them with the new status message.
    """
    form_class = CreateStatusMessageForm
    template_name = 'create_status_form.html'

    def get_context_data(self, **kwargs):
        """
        Adds the Profile object to the context using the profile's primary key (pk) from the URL.
        """
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']  # Retrieve profile ID from URL
        profile = Profile.objects.get(pk=pk)
        context['profile'] = profile  # Pass profile to template
        return context

    def form_valid(self, form):
        """
        Saves the StatusMessage associated with the correct Profile.
        Handles file uploads, creating corresponding Image and StatusImage objects.
        """
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        # Assign the profile to the new status message before saving
        status_message = form.save(commit=False)
        status_message.profile = profile
        status_message.save()

        # Process uploaded files (images)
        files = self.request.FILES.getlist('files')
        for f in files:
            img = Image()  # Create new Image object
            img.profile = profile  # Associate image with profile
            img.image_file = f  # Assign file to image object
            img.save()

            si = StatusImage()  # Create a StatusImage object linking image and status message
            si.status_message = status_message
            si.image = img
            si.save()

        return super().form_valid(form)

    def get_success_url(self):
        """
        Redirects to the profile page after successfully creating a status message.
        """
        pk = self.kwargs['pk']
        return reverse('show_profile', kwargs={'pk': pk})

class UpdateProfileView(UpdateView):
    """
    A view to update an existing Profile.
    Uses UpdateProfileForm for structured input.
    Redirects to the profile's get_absolute_url after saving.
    """
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'update_profile_form.html'

class UpdateStatusMessageView(UpdateView):
    """
    A view to update an existing StatusMessage.
    The update form only allows editing the message field.
    """
    model = StatusMessage
    form_class = UpdateStatusMessageForm
    template_name = 'update_status_form.html'

    def get_success_url(self):
        """
        Redirects to the profile page after updating the status message.
        """
        profile_pk = self.object.profile.pk  # Get associated profile ID
        return reverse('show_profile', kwargs={'pk': profile_pk})

class DeleteStatusMessageView(DeleteView):
    """
    A view to delete a StatusMessage.
    Displays a confirmation page before deletion.
    After confirmation, redirects to the profile page.
    """
    model = StatusMessage
    template_name = 'delete_status_form.html'
    context_object_name = 'status'  # Pass status message object to template

    def get_success_url(self):
        """
        Redirects to the profile page after deleting the status message.
        """
        profile_pk = self.object.profile.pk  # Get associated profile ID
        return reverse('show_profile', kwargs={'pk': profile_pk})
