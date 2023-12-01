# users/views.py
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .form import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, AdminNotificationForm
from .models import Notification, Profile

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            previous_wallet_balance = request.user.profile.wallet  # Store the previous wallet balance
            p_form.save()

            # Check if the wallet balance has changed
            if previous_wallet_balance != request.user.profile.wallet:
                # Create a notification for the user about the wallet balance change
                Notification.objects.create(
                    user=request.user,
                    message=f'Your wallet balance has been updated. New balance: {request.user.profile.wallet}'
                )

            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

@login_required
def notifications(request):
    user_notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'users/notifications.html', {'notifications': user_notifications})

@user_passes_test(lambda u: u.is_superuser)
def send_notification(request, user_id):
    if request.method == 'POST':
        form = AdminNotificationForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            user = User.objects.get(pk=user_id)
            Notification.objects.create(user=user, message=message)
            return redirect('profile')  # Redirect to the user's profile or any other page
    else:
        form = AdminNotificationForm()

    return render(request, 'users/send_notification.html', {'form': form})
def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'users/profile_update.html', {'form': form})