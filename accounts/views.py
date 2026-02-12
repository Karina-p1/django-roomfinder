# Import functions to render templates, redirect users, and authenticate
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages  # For flash messages

# -------------------------------
# USER REGISTRATION VIEW
# -------------------------------
def register(request):
    """
    Handles user registration.

    - Displays a registration form
    - Validates and saves new users
    - Shows success message after registration
    """
    # Create a registration form; populate with POST data if submitted
    form = UserCreationForm(request.POST or None)

    if form.is_valid():  # Check if submitted form is valid
        user = form.save()  # Save the new user to the database
        messages.success(request, "Registration successful. You can log in now.")  # Flash message
        return redirect('login')  # Redirect to login page after registration

    # If GET request or form invalid, render the registration page with the form
    return render(request, 'accounts/register.html', {'form': form})


# -------------------------------
# USER LOGIN VIEW
# -------------------------------
def user_login(request):
    """
    Handles user login with role-based redirection.

    - Authenticates credentials
    - Checks selected role against user type
    - Redirects admin users to admin dashboard
    - Redirects regular customers to room listing
    """
    if request.method == 'POST':
        # Get username, password, and role from submitted form
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')  # 'admin' or 'customer'

        # Authenticate user credentials
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Role-based redirection
            if role == 'admin' and (user.is_staff or user.is_superuser):
                login(request, user)  # Log in the admin user
                return redirect('dashboard')  # Redirect to admin dashboard
            elif role == 'customer' and not (user.is_staff or user.is_superuser):
                login(request, user)  # Log in the customer
                return redirect('room_list')  # Redirect to customer homepage
            else:
                messages.error(request, "Selected role does not match your account.")
        else:
            messages.error(request, "Invalid username or password.")

    # For GET request or invalid login, render login page
    return render(request, 'accounts/login.html')


# -------------------------------
# USER LOGOUT VIEW
# -------------------------------
def user_logout(request):
    """
    Logs out the current user and redirects to login page with a message.
    """
    logout(request)  # Log out user
    messages.info(request, "Logged out successfully.")  # Flash message
    return redirect('login')
