"""
File: apps.py
Author: Jane Pan (jjanepan@bu.edu)
Description: This file defines the configuration for the Mini Facebook application.
             It sets the default auto field and specifies the application name.
"""

from django.apps import AppConfig

class MiniFbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mini_fb'
