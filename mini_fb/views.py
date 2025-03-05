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
    context_object_name = 'profiles'

class ShowProfilePageView(DetailView):
    """
    Displays the details of a single Profile.
    """
    model = Profile
    template_name = 'show_profile.html'
    # Context object defaults to "object"

class CreateProfileView(CreateView):
    """
    A view to create a new Profile.
    After creation, it redirects to the profile's get_absolute_url.
    """
    form_class = CreateProfileForm
    template_name = 'create_profile_form.html'

class CreateStatusMessageView(CreateView):
    """
    A view to create a new StatusMessage, attaching it to the correct Profile.
    It also handles file uploads for images and creates corresponding Image and
    StatusImage objects.
    """
    form_class = CreateStatusMessageForm
    template_name = 'create_status_form.html'  # Must match your file name in templates

    def get_context_data(self, **kwargs):
        """
        Add the Profile object into the context, using the pk from the URL.
        """
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        context['profile'] = profile
        return context

    def form_valid(self, form):
        """
        Save the StatusMessage with the correct Profile, then process the
        uploaded files to create Image and StatusImage objects.
        """
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        status_message = form.save(commit=False)
        status_message.profile = profile
        status_message.save()

        # Handle image uploads from the form field named 'files'
        files = self.request.FILES.getlist('files')
        for f in files:
            # Create an Image object and save it
            img = Image()
            img.profile = profile
            img.image_file = f
            img.save()
            # Create a StatusImage object linking this image to the status message
            si = StatusImage()
            si.status_message = status_message
            si.image = img
            si.save()

        return super().form_valid(form)

    def get_success_url(self):
        """
        After creating the StatusMessage, redirect back to the profile page.
        """
        pk = self.kwargs['pk']
        return reverse('show_profile', kwargs={'pk': pk})

class UpdateProfileView(UpdateView):
    """
    A view to update an existing Profile.
    Uses UpdateProfileForm and, after saving, calls the model's get_absolute_url.
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
        After updating, redirect to the profile page associated with this status.
        """
        profile_pk = self.object.profile.pk
        return reverse('show_profile', kwargs={'pk': profile_pk})

class DeleteStatusMessageView(DeleteView):
    """
    A view to delete a StatusMessage.
    Shows a confirmation template and then redirects to the related profile page.
    """
    model = StatusMessage
    template_name = 'delete_status_form.html'
    context_object_name = 'status'

    def get_success_url(self):
        """
        After deletion, redirect back to the profile page.
        """
        profile_pk = self.object.profile.pk
        return reverse('show_profile', kwargs={'pk': profile_pk})

