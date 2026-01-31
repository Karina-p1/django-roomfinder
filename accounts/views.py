# render: render HTML templates; redirect: redirect to another page
from django.shortcuts import render, redirect
# built-in forms for signup/login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout  # functions to log in/out users

# -------------------------------
# REGISTER VIEW
# -------------------------------

def register(request):
    # Create a form instance; if POST data exists, populate it with that data
    form = UserCreationForm(request.POST or None)

    # Check if the submitted form is valid
    if form.is_valid():
        user = form.save()  # Save the new user to the database
        login(request, user)  # Log in the newly registered user automatically
        # Redirect to 'room_list' view after successful registration
        return redirect('room_list')

    # If GET request or form invalid, render the registration page with the form
    return render(request, 'accounts/register.html', {'form': form})


# -------------------------------
# LOGIN VIEW
# -------------------------------
def user_login(request):
    # Create an AuthenticationForm; bind POST data if submitted
    form = AuthenticationForm(request, data=request.POST or None)

    # If the form is valid (credentials correct)
    if form.is_valid():
        login(request, form.get_user())  # Log in the user
        return redirect('room_list')  # Redirect to 'room_list' after login

    # If GET request or credentials are wrong, render login page with the form
    return render(request, 'accounts/login.html', {'form': form})


# -------------------------------
# LOGOUT VIEW
# -------------------------------
def user_logout(request):
    logout(request)  # Log out the currently logged-in user
    return redirect('login')  # Redirect to login page after logout
