from django.urls import path         # Import path function to define URL routes
from . import views                  # Import views from this app

# List of URL patterns for this app
urlpatterns = [
    # URL: /         → Calls room_list view to show all rooms
    path('', views.room_list, name='room_list'),

    # URL: /add/     → Calls add_room view to add a new room
    path('add/', views.add_room, name='add_room'),

    # URL: /<id>/    → Calls room_detail view to show details of a specific room
    # <int:id> captures a number from the URL and passes it to the view
    path('<int:id>/', views.room_detail, name='room_detail'),
    
    # URL: /edit/<id>/ → Calls edit_room view to edit a room by its id
    path('edit/<int:id>/', views.edit_room, name='edit_room'),   

    # URL: /delete/<id>/ → Calls delete_room view to delete a room by its id
    path('delete/<int:id>/', views.delete_room, name='delete_room'),

    # URL: /         → Calls landing_page view to show available rooms
    path('', views.landing_page, name='landing_page'),
]
