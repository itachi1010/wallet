# users/urls.py

from django.urls import path
from .views import notifications, send_notification, register,profile_update

urlpatterns = [
    # Your existing URL patterns
    path('register/', register, name='register'),
    path('notifications/', notifications, name='notifications'),
    path('send_notification/<int:user_id>/', send_notification, name='send_notification'),
    path('profile/update/', profile_update, name='profile_update'),

]
