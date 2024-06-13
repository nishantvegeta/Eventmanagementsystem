from django import forms
from .models import Event

class EventForm(forms.Form):
    class Meta:
        model = Event
        field = ['title', 'description', 'total_participants', 'start_date', 'end_date']


class EventFilterForm(forms.Form):
    title = forms.CharField(required=False, label='Title')
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type':'date'}), label='Start Date')
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type':'date'}), label='End Date')



        