# users/views.py
import json
import os
import zipfile
from io import BytesIO
# users/views.py
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .form import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, AdminNotificationForm, CardForm
from .models import Notification, Card
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .form import TransactionForm
from .models import Transaction


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})





# ... other imports ...

@login_required
def profile(request):
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)
    card_form = CardForm()

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'card_form': card_form,
        'user_cards': Card.objects.filter(user=request.user),
    }

    if request.method == 'POST':
        card_form = CardForm(request.POST)
        if card_form.is_valid():
            card = card_form.save(commit=False)
            card.user = request.user
            card.save()
            messages.success(request, 'Your card has been added successfully!')
            return redirect('profile')  # Redirect to the profile page or any other page

    return render(request, 'users/profile.html', context)


@login_required
def update_card(request, card_id):
    card = get_object_or_404(Card, id=card_id, user=request.user)

    if request.method == 'POST':
        form = CardForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your card has been updated successfully!')
            return redirect('profile')  # Redirect to the profile page or any other page
    else:
        form = CardForm(instance=card)

    return render(request, 'users/update_card.html', {'form': form, 'card': card})


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


def add_card(request):
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            card.save()
            messages.success(request, 'Card details added successfully.')
            return redirect('blog-home')  # Change 'dashboard' to the name of your dashboard view
    else:
        form = CardForm()
    return render(request, 'users/card.html', {'form': form})

@login_required
def view_user_card(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Check if the current user is the owner of the profile or an administrator
    if request.user == user or request.user.is_superuser:
        user_cards = Card.objects.filter(user=user)
        return render(request, 'users/view_user_card.html', {'user': user, 'user_cards': user_cards})
    else:
        # Redirect or show an error message for unauthorized users
        messages.error(request, 'You are not authorized to view this user\'s cards.')
        return redirect('profile')  # Redirect to the user's profile or any other page


# @login_required
# @user_passes_test(lambda u: u.is_superuser)
# def view_user_card(request, user_id):
#     user = get_object_or_404(User, id=user_id)
#     user_cards = Card.objects.filter(user=user)
#     return render(request, 'users/view_user_card.html', {'user': user, 'user_cards': user_cards})


# users/views.py


@login_required
def send_money(request):
    if request.method == 'POST':
        # Process the form data
        form = TransactionForm(request.POST)

        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user

            # Check if the user has sufficient balance
            user_balance = request.user.profile.wallet
            amount = transaction.amount

            if amount > user_balance:
                messages.error(request, 'Insufficient balance.')
                return redirect('send_money')

            # Deduct the amount from the user's balance
            request.user.profile.wallet -= amount
            request.user.profile.save()

            # Create a transaction record
            transaction.save()

            messages.success(request, 'Transaction successful!')
            return redirect('send_money')


    else:
        form = TransactionForm(user=request.user)

    # If it's not a POST request, show the form
    return render(request, 'users/send_money.html', {'form': form})


def transaction_success(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    return render(request, 'users/transaction_success.html', {'transaction': transaction})
