from django import forms
from user.models import Video

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['upload_video_file']