# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile, Notification

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'wallet', 'image']
    search_fields = ['user__username']

    fieldsets = (
        ('User Information', {
            'fields': ('user', 'image'),
        }),
        ('Wallet Information', {
            'fields': ('wallet',),
        }),
    )

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'timestamp', 'is_read']
    search_fields = ['user__username']

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Notification, NotificationAdmin)
