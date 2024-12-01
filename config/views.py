from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, JsonResponse
from .forms import VideoForm
from user.models import Video
from user.tasks import process_video
import os


@login_required
def home(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # 업로드된 파일 저장
                video = form.save(commit=False)
                video.user = request.user
                video.save()

                # Celery 작업 큐에 추가
                process_video.delay(video.id)

                return JsonResponse({
                    'success': True,
                    'message': 'File uploaded successfully! Processing will begin shortly.'
                })
            except Exception as e:
                # 저장 중 발생한 예외 처리
                return JsonResponse({
                    'success': False,
                    'message': f'Error while saving video: {str(e)}'
                })
        else:
            # 폼 유효성 검사 실패
            return JsonResponse({
                'success': False,
                'message': f'Invalid form: {form.errors}'
            })

    # GET 요청 처리
    form = VideoForm()
    # 모든 비디오를 가져오되, 순서를 업로드 시간 기준으로 최신순 정렬
    videos = Video.objects.filter(user=request.user).order_by('-uploaded_at')

    return render(request, 'home.html', {
        'form': form,
        'videos': videos
    })


@login_required
def download_video(request, video_id):
    # 사용자가 선택한 비디오를 DB에서 가져옵니다.
    video = get_object_or_404(Video, id=video_id, user=request.user)

    # download_video_file이 존재하는지 확인합니다.
    if video.download_video_file:
        try:
            # 처리된 비디오 파일을 다운로드합니다.
            return FileResponse(open(video.download_video_file.path, "rb"), as_attachment=True)
        except FileNotFoundError:
            # 파일이 실제로 존재하지 않는 경우
            return JsonResponse({'error': 'The processed video file was not found.'}, status=404)
    else:
        # download_video_file이 아직 없는 경우
        return JsonResponse({'error': 'The processed video is not available yet.'}, status=400)
