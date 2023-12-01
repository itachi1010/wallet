# users/models.py

from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    wallet = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # New Fields
    full_name = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    identification_type = models.CharField(max_length=50, choices=[
        ('id_card', 'ID Card'),
        ('passport', 'Passport'),
        ('driver_license', 'Driver\'s License'),
    ], blank=True, null=True)
    id_front_image = models.ImageField(upload_to='user_identification/', blank=True, null=True)
    id_back_image = models.ImageField(upload_to='user_identification/', blank=True, null=True)
    selfie_with_id_image = models.ImageField(upload_to='user_identification/', blank=True, null=True)
    social_security_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message