"""
File: models.py
Author: Jane Pan
Description: This module defines the Voter model for the voter_analytics app,
             which represents registered voter records from the Newton voters CSV.
             It also includes a function to load data from the CSV file into the database.
"""

import os
import csv
from datetime import datetime
from django.db import models
from django.conf import settings

class Voter(models.Model):
    """
    Represents a registered voter in Newton.
    Fields are adapted from the CSV file:
    - Name fields
    - Residential Address fields
    - Dates for birth and registration
    - Party affiliation, precinct, election participation, and voter score
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    street_number = models.CharField(max_length=10, blank=True, null=True)
    street_name = models.CharField(max_length=100, blank=True, null=True)
    apt_number = models.CharField(max_length=10, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_registration = models.DateField(blank=True, null=True)
    party = models.CharField(max_length=50, blank=True, null=True)
    precinct = models.CharField(max_length=10, blank=True, null=True)
    
    # Election participation fields (as booleans)
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)
    
    voter_score = models.IntegerField(default=0)

    def __str__(self):
        """Returns a string representation of the Voter."""
        return f"{self.first_name} {self.last_name} (Score: {self.voter_score})"

def load_data():
    """
    Reads the newton_voters.csv file and creates Voter objects.
    Assumes the CSV file is located in the 'data' folder in the project root.
    Adjust field names and date formats to match your CSV headers.
    """
    # Construct the full file path: BASE_DIR/data/newton_voters.csv
    csv_file_path = os.path.join(settings.BASE_DIR, 'data', 'newton_voters.csv')
    
    with open(csv_file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert date strings to date objects, if possible.
            dob = None
            if row['Date of Birth']:
                try:
                    dob = datetime.strptime(row['Date of Birth'], '%Y-%m-%d').date()
                except Exception as e:
                    print("Error parsing Date of Birth:", e)
            
            reg_date = None
            if row['Date of Registration']:
                try:
                    reg_date = datetime.strptime(row['Date of Registration'], '%Y-%m-%d').date()
                except Exception as e:
                    print("Error parsing Date of Registration:", e)
            
            # Create and save the Voter object
            voter = Voter(
                first_name=row['First Name'],
                last_name=row['Last Name'],
                street_number=row['Residential Address - Street Number'],
                street_name=row['Residential Address - Street Name'],
                apt_number=row['Residential Address - Apartment Number'],
                zip_code=row['Residential Address - Zip Code'],
                date_of_birth=dob,
                date_of_registration=reg_date,
                party=row['Party Affiliation'],
                precinct=row['Precinct Number'],
                v20state=(row['v20state'] == 'TRUE'),
                v21town=(row['v21town'] == 'TRUE'),
                v21primary=(row['v21primary'] == 'TRUE'),
                v22general=(row['v22general'] == 'TRUE'),
                v23town=(row['v23town'] == 'TRUE'),
                voter_score=int(row['voter_score']) if row['voter_score'] else 0
            )
            voter.save()
