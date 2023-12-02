# users/views.py
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .form import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, AdminNotificationForm
from .models import Notification, Profile
from django.http import HttpResponse
from django.core.files import File
import json
import zipfile
import os
from io import BytesIO

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

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_page(request):
    users = User.objects.all()
    return render(request, 'users/admin_page.html', {'users': users})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'users/user_detail.html', {'user': user})



@login_required
@user_passes_test(lambda u: u.is_superuser)
def download_user_info(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Prepare user data
    user_data = {
        'username': user.username,
        'email': user.email,
        'phone_number': user.profile.phone_number,
        # ... add more fields as needed ...
    }

    # Prepare JSON file
    json_data = json.dumps(user_data, indent=2)
    json_file = BytesIO(json_data.encode())
    json_filename = f'{user.username}_info.json'

    # Prepare ZIP file
    zip_filename = f'{user.username}_info_and_images.zip'
    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        # Add JSON file to the ZIP
        zip_file.writestr(json_filename, json_data)

        # Add user images to the ZIP
        for image_field in ['id_front_image', 'id_back_image', 'selfie_with_id_image']:
            image = getattr(user.profile, image_field)
            if image:
                image_name = os.path.basename(image.name)
                zip_file.write(image.path, arcname=image_name)

    # Create HTTP response with ZIP file
    response = HttpResponse(zip_buffer.getvalue(), content_type='application/x-zip-compressed')
    response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'
    return response

