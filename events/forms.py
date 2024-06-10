from django.forms import forms
from .models import Event

class EventForm(forms.Form):
    class Meta:
        model = Event
        field = ['title', 'description', 'total_participants', 'start_date', 'end_date']