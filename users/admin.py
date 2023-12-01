# users/admin.py

from django.contrib import admin
from .models import Profile, Notification

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

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Notification, NotificationAdmin)
