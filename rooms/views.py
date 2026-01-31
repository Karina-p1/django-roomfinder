from django.shortcuts import render, redirect, get_object_or_404
# render  → renders HTML templates
# redirect → redirects to another URL
# get_object_or_404 → fetches object or returns 404 error if not found

from django.contrib.auth.decorators import login_required
# login_required ensures only logged-in users can access certain views

from .models import Room, RoomImage
# Import Room and RoomImage models from current app


# -------------------------------------
# ROOM LIST VIEW (with filtering)
# -------------------------------------
def room_list(request):
    # Fetch all rooms from database
    rooms = Room.objects.all()

    # Get filter values from URL query parameters
    location = request.GET.get('location')
    room_type = request.GET.get('room_type')

    # Filter rooms by location (case-insensitive search)
    if location:
        rooms = rooms.filter(location__icontains=location)

    # Filter rooms by room type (exact match)
    if room_type:
        rooms = rooms.filter(room_type=room_type)

    # Render room list template with filtered data
    return render(request, 'rooms/room_list.html', {
        'rooms': rooms,
        'location': location,
        'room_type': room_type
    })


# -------------------------------------
# ROOM DETAIL VIEW
# -------------------------------------
def room_detail(request, id):
    # Fetch a single room by ID or return 404 if not found
    room = get_object_or_404(Room, id=id)

    # Render room detail page
    return render(request, 'rooms/room_detail.html', {'room': room})


# -------------------------------------
# ADD ROOM VIEW
# -------------------------------------
@login_required
# Only logged-in users can add rooms
def add_room(request):
    # If form is submitted
    if request.method == 'POST':
        # Create a new Room object using form data
        room = Room.objects.create(
            owner=request.user,                 # Logged-in user is the owner
            title=request.POST['title'],
            description=request.POST['description'],
            price=request.POST['price'],
            location=request.POST['location'],
            room_type=request.POST['room_type'],
            owner_name=request.POST['owner_name'],
            contact_number=request.POST['contact_number'],
            available_from=request.POST['available_from']
        )

        # Save multiple uploaded images for the room
        for img in request.FILES.getlist('images'):
            RoomImage.objects.create(
                room=room,
                image=img
            )

        # Redirect to room list after successful creation
        return redirect('room_list')

    # If GET request, show empty add room form
    return render(request, 'rooms/add_room.html')


# -------------------------------------
# EDIT ROOM VIEW
# -------------------------------------
@login_required
# Only owner of the room can edit it
def edit_room(request, id):
    # Fetch room owned by the logged-in user
    room = get_object_or_404(Room, id=id, owner=request.user)

    # If form is submitted
    if request.method == 'POST':
        # Update room details
        room.title = request.POST['title']
        room.description = request.POST['description']
        room.price = request.POST['price']
        room.location = request.POST['location']
        room.room_type = request.POST['room_type']
        room.owner_name = request.POST['owner_name']
        room.contact_number = request.POST['contact_number']
        room.available_from = request.POST['available_from']
        room.save()  # Save changes to database

        # 🧹 Delete selected images
        delete_images = request.POST.getlist('delete_images')
        if delete_images:
            room.images.filter(id__in=delete_images).delete()

        # ➕ Add new images
        images = request.FILES.getlist('images')
        for img in images:
            RoomImage.objects.create(room=room, image=img)

        # Redirect to room detail page after update
        return redirect('room_detail', id=room.id)

    # If GET request, show edit form with existing data
    return render(request, 'rooms/edit_room.html', {'room': room})


# -------------------------------------
# DELETE ROOM VIEW
# -------------------------------------
@login_required
# Only owner can delete their room
def delete_room(request, id):
    # Fetch room owned by the logged-in user
    room = get_object_or_404(Room, id=id, owner=request.user)

    # Delete room from database
    room.delete()

    # Redirect back to room list
    return redirect('room_list')
