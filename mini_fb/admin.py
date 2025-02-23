# admin.py - Django Admin Configuration
# This file registers models to the Django admin interface 
# so they can be managed through the Django admin panel.

from django.contrib import admin  # Import Django's built-in admin module
from .models import Profile  # Import the Profile model from the current app's models

# Register the Profile model to make it accessible in the Django admin panel
admin.site.register(Profile)
