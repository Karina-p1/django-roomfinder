from django.db import models
from django.contrib.auth.models import User
# User model is used for authentication (login/register users)

# Room model represents a room listing in the database


class Room(models.Model):

    # Choices for room type (used as dropdown in forms)
    # First value → stored in database
    # Second value → shown to user
    ROOM_TYPE = [
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Shared', 'Shared'),
    ]

    # Choices for room location
    LOCATION_CHOICES = [
        ('Kathmandu', 'Kathmandu'),
        ('Pokhara', 'Pokhara'),
        ('Biratnagar', 'Biratnagar'),
    ]

    # Foreign key linking room to the user who created it
    # Each room belongs to one user,One user can have many rooms
    # ForeignKey = relationship on_delete=models.CASCADE = If user is deleted → their rooms are deleted too
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # Title of the room listing
    title = models.CharField(max_length=200)

    # Detailed description of the room
    description = models.TextField()

    # Monthly price of the room (only positive values allowed)
    price = models.PositiveIntegerField()

    # Location of the room (selected from LOCATION_CHOICES)
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES)

    # Type of room (Single / Double / Shared)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE)

    # Name of the room owner (displayed to users)
    owner_name = models.CharField(max_length=100)

    # Contact number of the owner (stored as text to allow +977 etc.)
    contact_number = models.CharField(max_length=15)

    # Date from which the room is available
    available_from = models.DateField()

    # Date and time when the room listing was created automatically
    created_at = models.DateTimeField(auto_now_add=True)

    # String representation of the room object
    # This is shown in Django admin panel

    def __str__(self):
        return self.title

# RoomImage model to store multiple images for each room


class RoomImage(models.Model):
    room = models.ForeignKey(
        Room, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='rooms/')
