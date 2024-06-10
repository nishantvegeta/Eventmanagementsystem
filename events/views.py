import os
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Event
from django.conf import settings
from django.shortcuts import redirect, render
from .forms import EventForm
from django.utils.dateparse import parse_date

@csrf_exempt
@require_http_methods(['GET', 'POST', 'PUT', 'DELETE'])
@login_required

def events(request):
    events_file_path = os.path.join(settings.BASE_DIR, 'events.json')
    
    if request.method == 'GET':
        events = read_events(events_file_path)

        title = request.GET.get('title')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if title:
            events = [event for event in events if event['title'] == title]

        if start_date:
            start_date_parsed = parse_date(start_date)
            events = [event for event in events if parse_date(event['start_date']) >= start_date_parsed]
        
        if end_date:
            end_date_parsed = parse_date(end_date)
            events = [event for event in events if parse_date(event['end_date']) <= end_date_parsed]
    
        return render(request, 'events/event_list.html', {'events':events})
    
    return HttpResponse(status = 405)


def home_page(request):
    return render(request, 'events/base.html', {})

@login_required
def create_event(request):
    events_file_path = os.path.join(settings.BASE_DIR, 'events.json')
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            events = read_events(events_file_path)
            events.append(data)
            write_events(events_file_path, events)
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form':form, 'event':None})
        
@login_required
def update_event(request, title):
    events_file_path = os.path.join(settings.BASE_DIR, 'events.json')
    events = read_events(events_file_path)
    event = next((event for event in events if event['title'] == title), None)
    if not event:
        return HttpResponse(status=404)
    
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            updated_data=form.cleaned_data
            for key, value in updated_data.items():
                event[key] = value
        write_events(events_file_path, events)
        return redirect('event_list')
    else:
        form = EventForm(initial=event)
        
    return render(request, 'events/event_form.html', {'form':form, 'event': event})

@login_required
def delete_event(request, title):
    events_file_path = os.path.join(settings.BASE_DIR, 'events.json')
    events = read_events(events_file_path)
    event = next((event for event in events if event['title'] == title), None)
    if not event:
        return HttpResponse(status=404)
    
    if request.method == 'POST':
        events.remove(event)
        write_events(events_file_path, events)
        return redirect('event_list')
    
    return render(request, 'events/event_confirm_delete.html', {'event': event})

def read_events(events_file_path):
    try:
        with open(events_file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def write_events(events_file_path, events):
    with open(events_file_path, 'w') as f:
        json.dump(events, f, indent=4)