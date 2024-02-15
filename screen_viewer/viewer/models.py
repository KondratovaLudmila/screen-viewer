from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Location(models.Model):
    full_name = models.CharField(max_length=200, unique=True)
    short_name = models.CharField(max_length=50, unique=True)
    path = models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.short_name


class Screenshot(models.Model):
    screen_date = models.DateField(null=True)
    path = models.CharField(max_length=200, unique=True)
    thmb_path = models.CharField(max_length=200, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    img_created_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        indexes=[models.Index(fields=['screen_date'], name='screen_date_idx')]