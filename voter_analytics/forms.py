"""
File: forms.py
Author: Jane Pan 
Description: Defines a form for filtering Voter records by various criteria.
"""

from django import forms
from datetime import datetime
from .models import Voter  # adjust if your model is named differently

VOTER_SCORE_CHOICES = [(i, str(i)) for i in range(6)]
YEAR_CHOICES = [(year, str(year)) for year in range(1900, datetime.now().year + 1)]

class VoterFilterForm(forms.Form):
    party = forms.ChoiceField(
        choices=[],
        required=False,
        label="Select Party Affiliation"
    )
    voter_score = forms.ChoiceField(
        choices=[('', 'Choose')] + VOTER_SCORE_CHOICES,
        required=False,
        label="Select Voter Score"
    )
    dob_min = forms.ChoiceField(
        choices=[('', 'Choose')] + YEAR_CHOICES[::-1],
        required=False,
        label="Min Year of Birth"
    )
    dob_max = forms.ChoiceField(
        choices=[('', 'Choose')] + YEAR_CHOICES[::-1],
        required=False,
        label="Max Year of Birth"
    )
    v20state = forms.BooleanField(required=False, label="v20state")
    v21town = forms.BooleanField(required=False, label="v21town")
    v21primary = forms.BooleanField(required=False, label="v21primary")
    v22general = forms.BooleanField(required=False, label="v22general")
    v23town = forms.BooleanField(required=False, label="v23town")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically set party choices from the database
        party_values = Voter.objects.values_list('party', flat=True).distinct()
        party_choices = sorted(set((code, code) for code in party_values if code))  # remove blanks
        self.fields['party'].choices = [('', 'Choose')] + party_choices
