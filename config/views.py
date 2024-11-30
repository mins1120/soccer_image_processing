from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, JsonResponse
from .forms import VideoForm
from user.models import Video

@login_required
def home(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user  # 현재 로그인한 사용자를 비디오에 연결
            video.save()
            return JsonResponse({'success': True, 'message': 'File uploaded successfully!'})

        return JsonResponse({'success': False, 'message': 'File upload failed. Please try again.'})
    
    else:
        form = VideoForm()
        videos = Video.objects.filter(user=request.user)

    return render(request, 'home.html', {
        'form': form,
        'videos': videos
    })

@login_required
def download_video(request, video_id):
    video = get_object_or_404(Video, id=video_id, user=request.user)
    return FileResponse(video.video_file, as_attachment=True)