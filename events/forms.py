from django.forms import forms
from .models import Event

class EventForm(forms.Form):
    class Meta:
        model = Event
        field = '__all__'