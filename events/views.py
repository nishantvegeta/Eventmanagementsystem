import os
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Event
from django.conf import settings
from django.shortcuts import redirect, render
from .forms import EventForm, EventFilterForm
from django.utils.dateparse import parse_date

@csrf_exempt
@require_http_methods(['GET', 'POST', 'PUT', 'DELETE'])
@login_required

def events(request):
    events_file_path = os.path.join(settings.BASE_DIR, 'events.json')
    events = read_events(events_file_path)

    filter_form = EventFilterForm(request.GET)
    if filter_form.is_valid():
        title = filter_form.cleaned_data.get('title')
        start_date = filter_form.cleaned_data.get('start_date')
        end_date = filter_form.cleaned_data.get('end_date')

        if title:
            events = [event for event in events if title.lower() in event['title'].lower()]
        if start_date:
            events = [event for event in events if event['start_date'] >= start_date.isoformate()]
        if end_date:
            events = [event for event in events if event['end_date'] <= end_date.isoformat()]

    return render(request, 'events/event_list.html', {'events':events, 'filter_form': filter_form})
    
 

def home_page(request):
    return render(request, 'events/base.html', {})

@login_required
def create_event(request):
    events_file_path = os.path.join(settings.BASE_DIR, 'events.json')
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        total_participants = request.POST.get('total_participants')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        events = read_events(events_file_path)
        new_id = max(event['id'] for event in events) + 1 if events else 1

        event = {
            'id': new_id,
            'title': title,
            'description': description,
            'total_participants': total_participants,
            'start_date': start_date,
            'end_date': end_date
        }

        events.append(event)
        write_events(events_file_path, events)
        return redirect('event_list')
    return render(request, 'events/event_form.html', {'event':None})
        
@login_required
def update_event(request, id):
    events_file_path = os.path.join(settings.BASE_DIR, 'events.json')
    events = read_events(events_file_path)
    event = next((event for event in events if event['id'] == int(id)), None)
    if not event:
        return HttpResponse(status=404)
    if request.method == 'GET':
     return render(request, 'events/event_form.html', { 'event': event})

    if request.method == 'POST':
        data = dict(request.POST)
        event_data = {key: value[0] for key, value in data.items()}
        event.update(event_data)  # Update the event dictionary directly
        write_events(events_file_path, events)  # Rewrite the JSON file with updated events
        return render(request, 'events/event_list.html', {'event': event})

    else:
        event = get_event(id)
        return render(request, 'events/event_list.html', {'event': event})


@login_required
def delete_event(request, id):
    events_file_path = os.path.join(settings.BASE_DIR, 'events.json')
    events = read_events(events_file_path)
    event = next((event for event in events if event['id'] == int(id)), None)
    if not event:
        return HttpResponse(status=404)
    if request.method == 'GET':
     return render(request, 'events/event_confirm_delete.html', { 'event': event})
    
    if request.method == 'POST':
        events.remove(event)
        write_events(events_file_path, events)
        return redirect('event_list')
    
    return redirect(request, 'events/event_list.html', {'event': event})

def read_events(events_file_path):
    try:
        with open(events_file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def write_events(events_file_path, events):
    with open(events_file_path, 'w') as f:
        json.dump(events, f, indent=4)



def get_event(title):
    # Load the events from the JSON file
    with open('events.json', 'r') as file:
        events = json.load(file)

    # Find the event with the matching title
    for event in events:
        if event['title'] == title:
            print(event)
        return event

    # If no event is found, return None
    return None