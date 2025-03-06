"""
models.py

This module defines the database models for the mini_fb application.

Models:
- Profile: Represents a user profile with basic information.
- StatusMessage: Represents a status message posted by a Profile.
- Image: Represents an uploaded image file associated with a Profile.
- StatusImage: A linking model that associates a StatusMessage with an Image.

Relationships:
- Each Profile can have multiple StatusMessages.
- Each Profile can upload multiple Images.
- Each StatusMessage can have multiple Images through the StatusImage linking table.

Dependencies:
- Django ORM (models.Model)
- Django utilities for date and URL handling (timezone, reverse)

Author: [Your Name]
Date: [Current Date]
"""

from django.db import models
from django.utils import timezone
from django.urls import reverse

class Profile(models.Model):
    """
    Represents a user profile with basic details such as name, city, 
    email, and an optional profile image URL.
    """
    first_name = models.CharField(max_length=50)  # First name of the profile owner
    last_name = models.CharField(max_length=50)   # Last name of the profile owner
    city = models.CharField(max_length=50)        # City where the profile owner resides
    email = models.EmailField(unique=True)        # Unique email for each profile
    profile_image_url = models.URLField(blank=True, null=True)  # Optional profile image URL

    def __str__(self):
        """Returns a string representation of the Profile."""
        return f"{self.first_name} {self.last_name}"

    def get_status_messages(self):
        """
        Returns all status messages associated with this Profile,
        ordered by newest first.
        """
        return self.statusmessage_set.order_by('-timestamp')

    def get_absolute_url(self):
        """
        Returns the URL to display this profile.
        Example: /mini_fb/profile/1
        """
        return reverse('show_profile', kwargs={'pk': self.pk})


class StatusMessage(models.Model):
    """
    Represents a status message posted by a Profile.
    A status message includes a timestamp and a text message.
    """
    timestamp = models.DateTimeField(default=timezone.now)  # Auto-set timestamp on creation
    message = models.TextField()  # Status message content
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)  # Links to Profile

    def __str__(self):
        """Returns a truncated representation of the status message."""
        return f"{self.profile.first_name}: {self.message[:50]}"

    def get_images(self):
        """
        Returns all Image objects related to this status message
        via the StatusImage relationship.
        """
        return Image.objects.filter(statusimage__status_message=self)


class Image(models.Model):
    """
    Represents an uploaded image file.
    An image is associated with a Profile and can have an optional caption.
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)  # Links to Profile
    image_file = models.ImageField(upload_to='images/')  # File path for uploaded images
    timestamp = models.DateTimeField(default=timezone.now)  # Auto-set timestamp on upload
    caption = models.CharField(max_length=200, blank=True)  # Optional image caption

    def __str__(self):
        """Returns a string representation of the Image object."""
        return f"Image {self.pk} for {self.profile}"


class StatusImage(models.Model):
    """
    A linking table that associates a StatusMessage with an Image.
    This allows a StatusMessage to have zero or many images.
    """
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)  # Links to StatusMessage
    image = models.ForeignKey(Image, on_delete=models.CASCADE)  # Links to Image

    def __str__(self):
        """Returns a string representation of the StatusImage relationship."""
        return f"StatusImage linking Status {self.status_message.pk} to Image {self.image.pk}"

    def get_images(self):
        """
        Returns all Images linked to this status via StatusImage.
        """
        return Image.objects.filter(statusimage__status_message=self)
