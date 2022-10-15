from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']

class UserDetails(models.Model):
    user = models.OneToOneField(User, related_name="details", on_delete=models.CASCADE)
    phone_number = models.IntegerField(default='')
    address = models.TextField(null=True, blank=True)
    upload_photo = models.ImageField(
        upload_to=settings.USER_PHOTO, null=True, blank=True)
    activation_key = models.CharField(max_length=100, blank=True, default='')
    activated = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
