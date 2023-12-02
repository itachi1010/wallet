# users/urls.py

from django.urls import path
from .views import notifications, send_notification, register, profile_update, admin_page, user_detail, \
    download_user_info

urlpatterns = [
    # Your existing URL patterns
    path('register/', register, name='register'),
    path('notifications/', notifications, name='notifications'),
    path('send_notification/<int:user_id>/', send_notification, name='send_notification'),
    path('profile/update/', profile_update, name='profile_update'),
    path('admin_page/', admin_page, name='admin_page'),
    path('user_detail/<int:user_id>/', user_detail, name='user_detail'),
    path('download_user_info/<int:user_id>/', download_user_info, name='download_user_info'),

]
