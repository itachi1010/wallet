# users/urls.py

from django.urls import path
from .views import notifications, send_notification

urlpatterns = [
    # Your existing URL patterns
    path('notifications/', notifications, name='notifications'),
    path('send_notification/<int:user_id>/', send_notification, name='send_notification'),

]
