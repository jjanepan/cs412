"""
File: admin.py
Author: Jane Pan (jjanepan@bu.edu)
Description: This file registers the Profile and StatusMessage models
             with the Django admin site, allowing them to be managed 
             through the Django admin interface.
"""

from django.contrib import admin
from .models import Profile, StatusMessage
from .models import Profile, StatusMessage, Image, StatusImage

# Register models with the Django admin site
admin.site.register(Profile)
admin.site.register(StatusMessage)
admin.site.register(Image)
admin.site.register(StatusImage)