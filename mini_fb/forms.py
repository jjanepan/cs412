"""
File: forms.py
Author: Jane Pan (jjanepan@bu.edu)
Description: This file defines Django forms for the Mini Facebook application.
             It includes forms for creating and managing user profiles and 
             status messages.
"""

from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    """
    A form to create a new Profile.
    """
    class Meta:
        model = Profile
        # Include all fields for the Profile model, or specify a subset:
        fields = ['first_name', 'last_name', 'city', 'email', 'profile_image_url']
class CreateStatusMessageForm(forms.ModelForm):
    """
    A form to create a new StatusMessage.
    We'll only ask the user for the message text;
    timestamp and profile will be set in the view.
    """
    class Meta:
        model = StatusMessage
        fields = ['message']

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        # exclude first_name, last_name if you don't want them updated
        fields = ['city', 'email', 'profile_image_url']

class UpdateStatusMessageForm(forms.ModelForm):
    class Meta:
        model = StatusMessage
        fields = ['message']  # only let user edit the text
