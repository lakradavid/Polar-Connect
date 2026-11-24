from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from .forms import LoginForm, RegisterForm, ProfileUpdateForm
from .models import CustomUser, Notification, Bookmark


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')

    if request.method == 'POST':
        # AuthenticationForm uses 'username' field name internally
        # but our form field is an EmailField named 'username'
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            remember = form.cleaned_data.get('remember_me')
            login(request, user)
            if not remember:
                request.session.set_expiry(0)
            messages.success(request, f'Welcome back, {user.get_display_name()}!')
            next_url = request.GET.get('next', '')
            return redirect(next_url if next_url else 'dashboard:index')
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
    else:
        form = LoginForm(request)

    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.full_name      = form.cleaned_data.get('full_name', '')
            user.phone_number   = form.cleaned_data.get('phone_number', '')
            user.institution    = form.cleaned_data.get('institution', '')
            user.designation    = form.cleaned_data.get('designation', '')
            user.user_category  = form.cleaned_data['user_category']

            # Map user_category → role
            cat_role_map = {
                'student':                'student',
                'researcher':             'researcher',
                'educator':               'educator',
                'scientific_professional':'researcher',
                'general_public':         'general_user',
            }
            user.role = cat_role_map.get(user.user_category, 'general_user')
            user.save()

            # Welcome notification
            Notification.objects.create(
                user=user,
                notification_type='general',
                title='Welcome to PolarConnect!',
                message=(
                    f'Hello {user.get_display_name()}, welcome to India\'s polar science portal. '
                    'Start by exploring the Knowledge Repository or Learning Centre.'
                ),
                link='/dashboard/',
            )

            login(request, user)
            messages.success(request, f'Account created successfully! Welcome, {user.get_display_name()}.')
            return redirect('dashboard:index')
        else:
            # Collect all field errors into one message so they show in the banner
            all_errors = []
            for field, errs in form.errors.items():
                label = form.fields[field].label if field in form.fields else field
                for err in errs:
                    all_errors.append(f'{label}: {err}')
            messages.error(request, ' | '.join(all_errors))
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'accounts/profile.html', {'form': form})
