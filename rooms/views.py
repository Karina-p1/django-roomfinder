from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import transaction
from .models import Room, RoomImage, Booking


# =========================================================
# ROLE-BASED DECORATORS
# =========================================================

def admin_required(view_func):
    """
    Allows access only to staff/superusers
    """
    return user_passes_test(lambda u: u.is_staff or u.is_superuser)(view_func)


def customer_required(view_func):
    """
    Allows access only to normal users (not admin)
    """
    return user_passes_test(lambda u: not (u.is_staff or u.is_superuser))(view_func)


# =========================================================
# AUTHENTICATION
# =========================================================

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, "Login successful!")

            # Role-based redirect
            if user.is_staff or user.is_superuser:
                return redirect("admin_dashboard")
            else:
                return redirect("room_list")

        messages.error(request, "Invalid credentials.")

    return render(request, "login.html")


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect("login")


# =========================================================
# ADMIN VIEWS
# =========================================================

@login_required
@admin_required
def dashboard(request):
    """
    Admin dashboard with statistics
    """
    rooms_count = Room.objects.count()
    bookings_count = Booking.objects.count()

    return render(request, "admin/dashboard.html", {
        "rooms_count": rooms_count,
        "bookings_count": bookings_count,
    })


@login_required
@admin_required
def manage_rooms(request):
    rooms = Room.objects.all()
    return render(request, "room_admin/manage_rooms.html", {"rooms": rooms})


@login_required
@admin_required
def manage_bookings(request):
    bookings = Booking.objects.select_related("user", "room")
    return render(request, "room_admin/manage_bookings.html", {"bookings": bookings})


@login_required
@admin_required
def approve_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    # Prevent double approval
    with transaction.atomic():
        already_approved = Booking.objects.filter(
            room=booking.room,
            status="Approved"
        ).exists()

        if already_approved:
            messages.error(request, "Room already approved for another booking.")
        else:
            booking.status = "Approved"
            booking.save()
            messages.success(request, "Booking approved successfully.")

    return redirect("manage_bookings")


@login_required
@admin_required
def reject_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = "Rejected"
    booking.save()
    messages.success(request, "Booking rejected successfully.")
    return redirect("manage_bookings")


@login_required
@admin_required
def add_room(request):
    if request.method == "POST":
        room = Room.objects.create(
            owner=request.user,
            title=request.POST["title"],
            description=request.POST["description"],
            price=request.POST["price"],
            location=request.POST["location"],
            room_type=request.POST["room_type"],
            owner_name=request.POST["owner_name"],
            contact_number=request.POST["contact_number"],
            available_from=request.POST["available_from"],
        )

        # Multiple image upload
        for img in request.FILES.getlist("images"):
            RoomImage.objects.create(room=room, image=img)

        messages.success(request, "Room added successfully.")
        return redirect("manage_rooms")

    return render(request, "room_admin/add_room.html")


@login_required
@admin_required
def edit_room(request, id):
    room = get_object_or_404(Room, id=id)

    if request.method == "POST":
        room.title = request.POST["title"]
        room.description = request.POST["description"]
        room.price = request.POST["price"]
        room.location = request.POST["location"]
        room.room_type = request.POST["room_type"]
        room.owner_name = request.POST["owner_name"]
        room.contact_number = request.POST["contact_number"]
        room.available_from = request.POST["available_from"]
        room.save()

        # Delete selected images
        delete_images = request.POST.getlist("delete_images")
        if delete_images:
            room.images.filter(id__in=delete_images).delete()

        # Add new images
        for img in request.FILES.getlist("images"):
            RoomImage.objects.create(room=room, image=img)

        messages.success(request, "Room updated successfully.")
        return redirect("manage_rooms")

    return render(request, "room_admin/edit_room.html", {"room": room})


@login_required
@admin_required
def delete_room(request, id):
    room = get_object_or_404(Room, id=id)
    room.delete()
    messages.success(request, "Room deleted successfully.")
    return redirect("manage_rooms")


# =========================================================
# CUSTOMER VIEWS
# =========================================================

@login_required
@customer_required
def customer_dashboard(request):
    return render(request, "customer/dashboard.html")


def room_list(request):
    rooms = Room.objects.all()

    # Filtering
    location = request.GET.get("location")
    room_type = request.GET.get("room_type")

    if location:
        rooms = rooms.filter(location__icontains=location)

    if room_type:
        rooms = rooms.filter(room_type=room_type)

    return render(request, "customer/room_list.html", {
        "rooms": rooms,
        "location": location,
        "room_type": room_type,
    })


def room_detail(request, id):
    room = get_object_or_404(Room, id=id)
    return render(request, "customer/room_detail.html", {"room": room})


@login_required
@customer_required
def book_room(request, id):
    room = get_object_or_404(Room, id=id)

    # Cannot book own room
    if room.owner == request.user:
        messages.error(request, "You cannot book your own room.")
        return redirect("room_detail", id=id)

    # Already approved booking
    if Booking.objects.filter(room=room, status="Approved").exists():
        messages.error(request, "This room is already booked.")
        return redirect("room_detail", id=id)

    # Already requested
    if Booking.objects.filter(room=room, user=request.user).exists():
        messages.warning(request, "You already requested this room.")
        return redirect("room_detail", id=id)

    Booking.objects.create(room=room, user=request.user, status="Pending")
    messages.success(request, "Booking request sent successfully.")
    return redirect("my_bookings")


@login_required
@customer_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, "customer/my_bookings.html", {"bookings": bookings})


@login_required
@customer_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if booking.status == "Pending":
        booking.delete()
        messages.success(request, "Booking cancelled successfully.")
    else:
        messages.error(request, "Only pending bookings can be cancelled.")

    return redirect("my_bookings")
