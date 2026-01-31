from django.urls import path  # Import Django's path function for URL routing
from . import views           # Import views from the current app (accounts)

# Define URL patterns for this app
urlpatterns = [
    # URL for user registration
    # Example: http://127.0.0.1:8000/register/
    # Calls the 'register' view function
    path('register/', views.register, name='register'),

    # URL for user login
    # Example: http://127.0.0.1:8000/login/
    # Calls the 'user_login' view function
    path('login/', views.user_login, name='login'),

    # URL for user logout
    # Example: http://127.0.0.1:8000/logout/
    # Calls the 'user_logout' view function
    path('logout/', views.user_logout, name='logout'),
]
