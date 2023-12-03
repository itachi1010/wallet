# users/urls.py

from django.urls import path
from .views import notifications, send_notification, register, profile_update, admin_page, user_detail, \
    download_user_info, add_card, view_user_card, send_money
from users import views as user_views
from users.views import update_card
from django.contrib.auth import views as auth_views


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
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('update_card/<int:card_id>/', update_card, name='update_card'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ),
         name='password_reset_complete'),

]
