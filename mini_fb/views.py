"""
File: views.py
Author: Jane Pan (jjanepan@bu.edu)
Description: This module contains Django class-based views for handling Profile and
             StatusMessage operations, as well as managing friend relationships and
             displaying a news feed. It includes views for listing, creating, updating,
             and deleting profiles and status messages, handling image uploads, and
             supporting friend suggestions and adding friends.
Date: [Current Date]
"""

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.views import View
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
    context_object_name = 'profiles'

class ShowProfilePageView(DetailView):
    """
    Displays the details of a single Profile.
    """
    model = Profile
    template_name = 'show_profile.html'
    # The context object defaults to "object"

class CreateProfileView(CreateView):
    """
    A view to create a new Profile using CreateProfileForm.
    After creation, it redirects to the profile's get_absolute_url.
    """
    form_class = CreateProfileForm
    template_name = 'create_profile_form.html'

class CreateStatusMessageView(CreateView):
    """
    A view to create a new StatusMessage and attach it to the correct Profile.
    Handles image uploads and creates corresponding Image and StatusImage objects.
    """
    form_class = CreateStatusMessageForm
    template_name = 'create_status_form.html'

    def get_context_data(self, **kwargs):
        """
        Adds the Profile object to the context using the profile's primary key (pk)
        from the URL.
        """
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']  # Retrieve profile ID from URL
        profile = Profile.objects.get(pk=pk)
        context['profile'] = profile
        return context

    def form_valid(self, form):
        """
        Saves the StatusMessage with the correct Profile.
        Processes uploaded files (from the 'files' field) to create Image and StatusImage objects.
        """
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        status_message = form.save(commit=False)
        status_message.profile = profile
        status_message.save()

        # Process uploaded files (if any)
        files = self.request.FILES.getlist('files')
        for f in files:
            # Create and save an Image object
            img = Image()
            img.profile = profile
            img.image_file = f
            img.save()
            # Create a linking StatusImage object
            si = StatusImage()
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
    A view to update an existing Profile using UpdateProfileForm.
    Redirects to the profile's get_absolute_url after saving.
    """
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'update_profile_form.html'

class UpdateStatusMessageView(UpdateView):
    """
    A view to update an existing StatusMessage.
    Only the message field is editable.
    """
    model = StatusMessage
    form_class = UpdateStatusMessageForm
    template_name = 'update_status_form.html'

    def get_success_url(self):
        """
        After updating the status message, redirect to the associated profile page.
        """
        profile_pk = self.object.profile.pk
        return reverse('show_profile', kwargs={'pk': profile_pk})

class DeleteStatusMessageView(DeleteView):
    """
    A view to delete a StatusMessage.
    Displays a confirmation page and, upon deletion, redirects to the profile page.
    """
    model = StatusMessage
    template_name = 'delete_status_form.html'
    context_object_name = 'status'

    def get_success_url(self):
        """
        After deletion, redirect to the associated profile page.
        """
        profile_pk = self.object.profile.pk
        return reverse('show_profile', kwargs={'pk': profile_pk})

class ShowNewsFeedView(DetailView):
    """
    Displays the news feed for a given Profile, which includes status messages
    from the profile and its friends.
    """
    model = Profile
    template_name = 'news_feed.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_feed'] = self.object.get_news_feed()
        return context

class ShowFriendSuggestionsView(DetailView):
    """
    Displays friend suggestions for a given Profile.
    """
    model = Profile
    template_name = 'friend_suggestions.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['suggestions'] = self.object.get_friend_suggestions()
        return context

class AddFriendView(View):
    """
    A view to add a friend relationship between two Profiles.
    Expects URL parameters: pk (the current profile's ID) and other_pk (the friend-to-add's ID).
    """
    def get(self, request, pk, other_pk):
        profile = get_object_or_404(Profile, pk=pk)
        other = get_object_or_404(Profile, pk=other_pk)
        try:
            profile.add_friend(other)
        except ValueError:
            # Optionally handle self-friending error or duplicates here.
            pass
        return redirect('show_profile', pk=pk)
