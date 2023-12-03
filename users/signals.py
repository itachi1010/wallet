from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Transaction, Notification


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    # Check if the associated Profile instance exists
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        # If not, you might want to create a profile here
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Transaction)
def notify_admin(sender, instance, created, **kwargs):
    # if not created:
    admin_user = User.objects.get(username='benny')  # Replace 'admin' with your actual admin username
    message = f"New transaction by {instance.user.username}. Amount: ${instance.amount}"
    notifiaction = Notification.objects.create(user=admin_user, message=message)
    print(f'{admin_user}, just received a notification')
    print(message, notifiaction)

