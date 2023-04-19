from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import logout

from accounts.forms import UserRegistrationForm


def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, "Login failed, please try again.")
            return render(request, 'accounts/login.html', {})
    else:
        return render(request, 'accounts/login.html', {})


def logout_view(request):
    logout(request)
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            login(request, new_user, backend='accounts.authentication.EmailAuthBackEnd')
            return render(request,
                          'home.html',
                          {'new_user': new_user})
        else:
            messages.success(request, "Registration failed, please try again.")
            return render(request, 'accounts/register.html', {})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'accounts/register.html',
                  {'user_form': user_form})
