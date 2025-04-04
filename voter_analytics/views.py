"""
File: views.py
Author: Jane Pan
Description: Views for listing, filtering, and displaying Voter records.
"""

import plotly.express as px
from plotly.offline import plot
from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django.db.models import Q
from django.db.models import Count
from .models import Voter
from .forms import VoterFilterForm

class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100  # pages of 100 records

    def get_queryset(self):
        qs = super().get_queryset()
        form = self.get_filter_form()
        if form.is_valid():
            data = form.cleaned_data
            # Filter by party
            if data['party']:
                qs = qs.filter(party=data['party'])
            # Filter by date of birth range
            if data['dob_min']:
                qs = qs.filter(date_of_birth__year__gte=data['dob_min'])
            if data['dob_max']:
                qs = qs.filter(date_of_birth__year__lte=data['dob_max'])
            # Filter by voter_score
            if data['voter_score']:
                qs = qs.filter(voter_score=int(data['voter_score']))
            # Filter by elections
            if data['v20state']:
                qs = qs.filter(v20state=True)
            if data['v21town']:
                qs = qs.filter(v21town=True)
            if data['v21primary']:
                qs = qs.filter(v21primary=True)
            if data['v22general']:
                qs = qs.filter(v22general=True)
            if data['v23town']:
                qs = qs.filter(v23town=True)
        return qs

    def get_filter_form(self):
        # Build the form from GET parameters
        return VoterFilterForm(self.request.GET or None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["distinct_parties"] = (
            Voter.objects.values_list("party", flat=True)
            .distinct()
            .order_by("party")
        )
        return context

class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'

class VoterGraphsView(ListView):
    """
    Displays graphs of Voter data.
    Includes:
      1. A histogram of voter birth years.
      2. A pie chart of party distribution.
      3. A bar chart of election participation.
    Reuses filtering logic from VoterListView.
    """
    model = Voter
    template_name = 'voter_analytics/voter_graphs.html'
    context_object_name = 'voters'

    def get_queryset(self):
        qs = super().get_queryset()
        form = VoterFilterForm(self.request.GET or None)
        if form.is_valid():
            data = form.cleaned_data
            if data['party']:
                qs = qs.filter(party=data['party'])
            if data['dob_min']:
                qs = qs.filter(date_of_birth__year__gte=data['dob_min'])
            if data['dob_max']:
                qs = qs.filter(date_of_birth__year__lte=data['dob_max'])
            if data['voter_score']:
                qs = qs.filter(voter_score=int(data['voter_score']))
            if data['v20state']:
                qs = qs.filter(v20state=True)
            if data['v21town']:
                qs = qs.filter(v21town=True)
            if data['v21primary']:
                qs = qs.filter(v21primary=True)
            if data['v22general']:
                qs = qs.filter(v22general=True)
            if data['v23town']:
                qs = qs.filter(v23town=True)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.object_list

        # Provide the filter form for re-filtering on the graphs page
        context['filter_form'] = VoterFilterForm(self.request.GET or None)

        # 1) Birth Year Histogram
        birth_years = [v.date_of_birth.year for v in qs if v.date_of_birth]
        if birth_years:
            fig = px.histogram(x=birth_years, nbins=40, 
                               labels={'x': 'Birth Year', 'y': 'Count'},
                               title='Birth Year Distribution')
            context['birth_year_hist'] = plot(fig, output_type='div')

        # 2) Party Distribution Pie Chart
        # We use a group-by aggregation to count voters by party.
        party_counts = qs.values('party').annotate(count=Count('party'))
        if party_counts:
            fig2 = px.pie(party_counts, names='party', values='count', title='Party Distribution')
            context['party_pie'] = plot(fig2, output_type='div')

        # 3) Election Participation Bar Chart
        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        participation = {}
        for election in elections:
            participation[election] = qs.filter(**{election: True}).count()
        if participation:
            fig3 = px.bar(x=list(participation.keys()), y=list(participation.values()),
                          labels={'x': 'Election', 'y': 'Number of Voters'},
                          title='Voter Participation by Election')
            context['election_bar'] = plot(fig3, output_type='div')

        return context