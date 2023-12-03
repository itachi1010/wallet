# users/urls.py

from django.urls import path
from .views import notifications, send_notification, register, profile_update, admin_page, user_detail, \
    download_user_info, add_card, view_user_card, send_money

urlpatterns = [
    # Your existing URL patterns
    path('send_money/', send_money, name='send_money'),
    path('register/', register, name='register'),
    path('notifications/', notifications, name='notifications'),
    path('send_notification/<int:user_id>/', send_notification, name='send_notification'),
    path('profile/update/', profile_update, name='profile_update'),
    path('admin_page/', admin_page, name='admin_page'),
    path('user_detail/<int:user_id>/', user_detail, name='user_detail'),
    path('download_user_info/<int:user_id>/', download_user_info, name='download_user_info'),
    path('add_card/', add_card, name='add_card'),
    path('view_user_card/<int:user_id>/', view_user_card, name='view_user_card'),

]
