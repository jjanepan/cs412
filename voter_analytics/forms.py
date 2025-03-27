"""
File: forms.py
Author: Jane Pan 
Description: Defines a form for filtering Voter records by various criteria.
"""

from django import forms

# Example choices for date ranges or parties, adapt as needed
PARTY_CHOICES = [
    ('', 'Any'),
    ('D', 'Democrat'),
    ('R', 'Republican'),
    ('U', 'Unaffiliated'),
]

SCORE_CHOICES = [
    ('', 'Any'),
    ('0', '0'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
]

class VoterFilterForm(forms.Form):
    party = forms.ChoiceField(choices=PARTY_CHOICES, required=False, label="Party")
    dob_min = forms.IntegerField(required=False, label="Min Birth Year")
    dob_max = forms.IntegerField(required=False, label="Max Birth Year")
    voter_score = forms.ChoiceField(choices=SCORE_CHOICES, required=False, label="Voter Score")
    
    # Checkboxes for elections
    v20state = forms.BooleanField(required=False, label="Voted in 2020 State")
    v21town = forms.BooleanField(required=False, label="Voted in 2021 Town")
    v21primary = forms.BooleanField(required=False, label="Voted in 2021 Primary")
    v22general = forms.BooleanField(required=False, label="Voted in 2022 General")
    v23town = forms.BooleanField(required=False, label="Voted in 2023 Town")
