from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),  # main landing page
    path('bookings/', views.booking_list, name='booking_list'),
]
