import base64                      # Used to convert images to base64 for HTML display
import io                          # Used for in-memory image storage
import matplotlib.pyplot as plt   # Used to generate charts
from django.shortcuts import render
from django.db.models import Count
from rooms.models import Room, Booking
from django.contrib.auth.decorators import login_required
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend for server


def dashboard_view(request):

    # ============================
    # 1️ TOP SUMMARY NUMBERS
    # ============================

    # Total number of rooms in the system
    total_rooms = Room.objects.count()

    # Find the most popular room type
    # Groups rooms by room_type and counts them
    popular_type = (
        Room.objects
        .values('room_type')
        .annotate(total=Count('id'))
        .order_by('-total')
        .first()
    )

    # Find the location with the highest number of rooms
    # Groups rooms by location and counts them
    popular_location = (
        Room.objects
        .values('location')
        .annotate(total=Count('id'))
        .order_by('-total')
        .first()
    )

    # ============================
    # 2️ ROOMS BY TYPE CHART
    # ============================

    # Define room types manually
    room_types = ['Single', 'Double', 'Shared']

    # Count rooms for each room type
    type_counts = [
        Room.objects.filter(room_type=rt).count()
        for rt in room_types
    ]

    # Create bar chart
    plt.figure(figsize=(6, 4))
    bars = plt.bar(room_types, type_counts, color=[
                   '#4CAF50', '#2196F3', '#FF9800'])

    # Chart styling
    plt.title('Rooms by Type')
    plt.ylabel('Count')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Calculate total rooms (for percentage)
    total = sum(type_counts)

    # Add count and percentage labels above bars
    for bar, count in zip(bars, type_counts):
        percent = (count / total * 100) if total > 0 else 0
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.1,
            f'{count} ({percent:.1f}%)',
            ha='center'
        )

    # Save chart to memory (not file system)
    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Convert image to base64 so it can be embedded in HTML
    type_chart = base64.b64encode(buffer.getvalue()).decode()

    buffer.close()
    plt.close()   # Free memory

    # ============================
    # 3️ ROOMS BY LOCATION CHART
    # ============================

    # Define locations manually
    locations = ['Kathmandu', 'Pokhara', 'Biratnagar']

    # Count rooms in each location
    location_counts = [
        Room.objects.filter(location=loc).count()
        for loc in locations
    ]

    # Create bar chart
    plt.figure(figsize=(6, 4))
    bars = plt.bar(locations, location_counts, color=[
                   '#F44336', '#3F51B5', '#FFC107'])

    # Chart styling
    plt.title('Rooms by Location')
    plt.ylabel('Count')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Calculate total rooms (for percentage)
    total_loc = sum(location_counts)

    # Add count and percentage labels above bars
    for bar, count in zip(bars, location_counts):
        percent = (count / total_loc * 100) if total_loc > 0 else 0
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.1,
            f'{count} ({percent:.1f}%)',
            ha='center'
        )

    # Save chart to memory
    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Convert image to base64
    location_chart = base64.b64encode(buffer.getvalue()).decode()

    buffer.close()
    plt.close()   # Free memory

    # ============================
    # 4️ SEND DATA TO TEMPLATE
    # ============================

    context = {
        'total_rooms': total_rooms,           # Total rooms count
        'popular_type': popular_type,         # Most common room type
        'popular_location': popular_location,  # Location with most rooms
        'type_chart': type_chart,              # Base64 room type chart
        'location_chart': location_chart,      # Base64 location chart
    }

@login_required
def booking_list(request):

    # Super admin → see all bookings
    if request.user.is_staff:
        bookings = Booking.objects.all()

    # Room owner → see bookings for their rooms
    else:
        bookings = Booking.objects.filter(
            room__owner=request.user
        )

    return render(
        request,
        'dashboard/bookings.html',
        {'bookings': bookings}
    )

@login_required
def dashboard_view(request):

    # ============================
    # 1️ TOP SUMMARY NUMBERS
    # ============================

    total_rooms = Room.objects.count()

    popular_type = (
        Room.objects
        .values('room_type')
        .annotate(total=Count('id'))
        .order_by('-total')
        .first()
    )

    popular_location = (
        Room.objects
        .values('location')
        .annotate(total=Count('id'))
        .order_by('-total')
        .first()
    )

    # ============================
    # 2️ ROOMS BY TYPE CHART
    # ============================

    room_types = ['Single', 'Double', 'Shared']

    type_counts = [
        Room.objects.filter(room_type=rt).count()
        for rt in room_types
    ]

    plt.figure(figsize=(6, 4))
    bars = plt.bar(room_types, type_counts, color=[
                   '#4CAF50', '#2196F3', '#FF9800'])

    plt.title('Rooms by Type')
    plt.ylabel('Count')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    total = sum(type_counts)

    for bar, count in zip(bars, type_counts):
        percent = (count / total * 100) if total > 0 else 0
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.1,
            f'{count} ({percent:.1f}%)',
            ha='center'
        )

    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    type_chart = base64.b64encode(buffer.getvalue()).decode()

    buffer.close()
    plt.close()

    # ============================
    # 3️ ROOMS BY LOCATION CHART
    # ============================

    locations = ['Kathmandu', 'Pokhara', 'Biratnagar']

    location_counts = [
        Room.objects.filter(location=loc).count()
        for loc in locations
    ]

    plt.figure(figsize=(6, 4))
    bars = plt.bar(locations, location_counts, color=[
                   '#F44336', '#3F51B5', '#FFC107'])

    plt.title('Rooms by Location')
    plt.ylabel('Count')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    total_loc = sum(location_counts)

    for bar, count in zip(bars, location_counts):
        percent = (count / total_loc * 100) if total_loc > 0 else 0
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.1,
            f'{count} ({percent:.1f}%)',
            ha='center'
        )

    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    location_chart = base64.b64encode(buffer.getvalue()).decode()

    buffer.close()
    plt.close()

    # ============================
    # 4️ SEND DATA TO TEMPLATE
    # ============================

    context = {
        'total_rooms': total_rooms,
        'popular_type': popular_type,
        'popular_location': popular_location,
        'type_chart': type_chart,
        'location_chart': location_chart,
    }

    return render(request, 'dashboard/dashboard.html', context)

