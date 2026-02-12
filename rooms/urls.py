from django.urls import path
from . import views

urlpatterns = [
path('', views.room_list, name='room_list'),  # Homepage
    # =====================================================
    # AUTHENTICATION
    # =====================================================
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),


    # =====================================================
    # ADMIN SECTION
    # =====================================================

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Room management
    path('manage-rooms/', views.manage_rooms, name='manage_rooms'),
    path('add-room/', views.add_room, name='add_room'),
    path('edit-room/<int:id>/', views.edit_room, name='edit_room'),
    path('delete-room/<int:id>/', views.delete_room, name='delete_room'),

    # Booking management
    path('manage-bookings/', views.manage_bookings, name='manage_bookings'),
    path('approve/<int:booking_id>/', views.approve_booking, name='approve_booking'),
    path('reject/<int:booking_id>/', views.reject_booking, name='reject_booking'),


    # =====================================================
    # CUSTOMER SECTION
    # =====================================================

    # Customer dashboard
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),

    # Room browsing
    path('', views.room_list, name='room_list'),  # Home page
    path('room/<int:id>/', views.room_detail, name='room_detail'),

    # Booking actions
    path('book/<int:id>/', views.book_room, name='book_room'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]
