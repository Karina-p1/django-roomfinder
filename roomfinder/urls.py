"""
URL configuration for roomfinder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include  # include is needed to reference app URLs
from django.conf import settings
from django.conf.urls.static import static
# For built-in login/logout views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),

    # Dashboard landing page (for admins)
    path('', include('dashboard.urls')),  # e.g., http://127.0.0.1:8000/

    # Rooms app (list, details, add room, etc.)
    # e.g., http://127.0.0.1:8000/rooms/
    path('rooms/', include('rooms.urls')),

    # Accounts app URLs (register, login, logout)
    path('accounts/', include('accounts.urls')),
    # This makes URLs like:
    # /accounts/register/ -> register view
    # /accounts/login/    -> login view
    # /accounts/logout/   -> logout view

    # Optional: If you want to use Django's built-in LoginView/LogoutView instead of custom ones
    # path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    # path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
