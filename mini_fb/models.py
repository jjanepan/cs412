# mini_fb/models.py

from django.db import models
from django.utils import timezone
from django.urls import reverse

class Profile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    profile_image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_status_messages(self):
        """
        Return all status messages associated with this Profile,
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
    timestamp = models.DateTimeField(default=timezone.now)
    message = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        # Return the first 50 chars of the message for readability
        return f"{self.profile.first_name}: {self.message[:50]}"
