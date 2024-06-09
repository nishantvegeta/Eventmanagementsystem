from django.urls import path
from . import views
from events.views import events

urlpatterns = [
    path('event/', views.events, name='event_list'),
    path('event/create', views.create_event, name='event_create'),
    path('event/update/<str:title>/', views.update_event, name='event_update'),
    path('event/delete/<str:title>/', views.delete_event, name='event_delete'),
]