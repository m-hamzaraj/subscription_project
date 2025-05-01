from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)  # Approval by admin
    payment_id = models.CharField(max_length=255, blank=True, null=True)
    payment_screenshot = models.ImageField(upload_to='payments/', blank=True, null=True)

    def is_active(self):
        return self.is_approved and self.end_date and now() < self.end_date

    def __str__(self):
        return f"{self.user.username}'s Subscription"


from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    banner_image = models.ImageField(upload_to='video_banners/', null=True, blank=True)  # Add this
    video_file = models.FileField(upload_to='videos/')  # Assuming videos are stored locally

    def __str__(self):
        return self.title

