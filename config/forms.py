from django import forms
from user.models import Video

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['video_file']