from django.db import models
from django.conf import settings

class Video(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    upload_video_file = models.FileField(upload_to='videos/')
    download_video_file = models.FileField(upload_to='processed_videos/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)