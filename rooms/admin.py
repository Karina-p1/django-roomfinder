# Import Django admin module to register models in admin interface
from django.contrib import admin
# Register your models here.
# Import the Room and RoomImage models from the same app
from .models import Room, RoomImage

# Create an inline admin interface for RoomImage
# RoomImageInline → lets you add multiple images while editing a single Room.
# This allows adding RoomImage(s) directly when editing a Room
class RoomImageInline(admin.TabularInline):
    model = RoomImage   # Specify which model this inline is for
    extra = 1           # Number of extra empty forms to show for adding new images. Shows one blank image form by default; you can add more.

# Create a custom admin interface for Room
class RoomAdmin(admin.ModelAdmin):
    inlines = [RoomImageInline] # Include the RoomImageInline so images can be managed within Room

# Register the Room model with the custom RoomAdmin in Django admin
# This enables you to manage Rooms and their images in the admin panel
admin.site.register(Room, RoomAdmin)
