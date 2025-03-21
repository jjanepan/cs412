"""
File: models.py
Author: Jane Pan (jjanepan@bu.edu)
Description: This module defines the database models for the mini_fb application.
             Models include:
             - Profile: Represents a user profile with basic details.
             - StatusMessage: Represents a status message posted by a Profile.
             - Image: Represents an uploaded image file associated with a Profile.
             - StatusImage: A linking model associating a StatusMessage with an Image.
             - Friend: Represents a friendship between two Profiles.
             
             Additional methods are provided on the Profile model:
             - get_status_messages(): Returns all status messages for the profile.
             - get_friends(): Returns a QuerySet of Profiles that are friends.
             - add_friend(other): Creates a friendship with another Profile.
             - get_friend_suggestions(): Returns Profiles that are not already friends.
             - get_news_feed(): Returns status messages from the profile and its friends.
             
Dependencies:
- Django ORM (models.Model)
- Django utilities for time and URL handling (timezone, reverse)
"""

from django.db import models
from django.utils import timezone
from django.urls import reverse

class Profile(models.Model):
    """
    Represents a user profile with basic details such as name, city, email,
    and an optional profile image URL.
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
        Example: /mini_fb/profile/1/
        """
        return reverse('show_profile', kwargs={'pk': self.pk})

    def get_friends(self):
        """
        Returns a QuerySet of Profiles that are friends with this Profile.
        It checks both Friend relations where self appears as either profile1 or profile2.
        """
        from django.db.models import Q
        friend_relations = Friend.objects.filter(Q(profile1=self) | Q(profile2=self))
        friend_ids = []
        for fr in friend_relations:
            if fr.profile1 == self:
                friend_ids.append(fr.profile2.pk)
            else:
                friend_ids.append(fr.profile1.pk)
        return Profile.objects.filter(pk__in=friend_ids)

    def add_friend(self, other):
        """
        Creates a friendship between self and another Profile 'other'.
        Prevents self-friending and duplicate relationships.
        """
        if self == other:
            raise ValueError("Cannot add yourself as a friend.")
        from django.db.models import Q
        if Friend.objects.filter(Q(profile1=self, profile2=other) | Q(profile1=other, profile2=self)).exists():
            return  # Already friends; do nothing.
        Friend.objects.create(profile1=self, profile2=other)

    def get_friend_suggestions(self):
        """
        Returns a QuerySet of Profiles that are not already friends with this Profile
        and excludes self.
        """
        all_profiles = Profile.objects.exclude(pk=self.pk)
        current_friend_ids = self.get_friends().values_list('pk', flat=True)
        return all_profiles.exclude(pk__in=current_friend_ids)

    def get_news_feed(self):
        """
        Returns a QuerySet of StatusMessages from this Profile and its friends,
        ordered by newest first.
        """
        friend_ids = self.get_friends().values_list('pk', flat=True)
        relevant_ids = list(friend_ids) + [self.pk]
        return StatusMessage.objects.filter(profile__pk__in=relevant_ids).order_by('-timestamp')


class StatusMessage(models.Model):
    """
    Represents a status message posted by a Profile.
    """
    timestamp = models.DateTimeField(default=timezone.now)  # Timestamp when the message was created
    message = models.TextField()  # Text content of the status message
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)  # The profile that posted the status

    def __str__(self):
        """Returns a truncated representation of the status message."""
        return f"{self.profile.first_name}: {self.message[:50]}"

    def get_images(self):
        """
        Returns all Image objects associated with this StatusMessage via the StatusImage relationship.
        """
        return Image.objects.filter(statusimage__status_message=self)


class Image(models.Model):
    """
    Represents an uploaded image file.
    An image is associated with a Profile and may have an optional caption.
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)  # The profile that uploaded the image
    image_file = models.ImageField(upload_to='images/')  # Uploaded image stored in media/images/
    timestamp = models.DateTimeField(default=timezone.now)  # Timestamp when the image was uploaded
    caption = models.CharField(max_length=200, blank=True)  # Optional caption for the image

    def __str__(self):
        """Returns a string representation of the Image object."""
        return f"Image {self.pk} for {self.profile}"


class StatusImage(models.Model):
    """
    A linking model that associates a StatusMessage with an Image.
    Allows a StatusMessage to have zero or many images.
    """
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)  # Links to a status message
    image = models.ForeignKey(Image, on_delete=models.CASCADE)  # Links to an image

    def __str__(self):
        """Returns a string representation of the StatusImage relationship."""
        return f"StatusImage linking Status {self.status_message.pk} to Image {self.image.pk}"


class Friend(models.Model):
    """
    Represents a friendship between two Profiles.
    """
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friend_profile1')
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friend_profile2')
    timestamp = models.DateTimeField(default=timezone.now)  # Timestamp of when the friendship was created

    def __str__(self):
        """Returns a string representation of the Friend relationship."""
        return f"{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name}"
