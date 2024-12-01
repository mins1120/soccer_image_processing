from celery import shared_task
import subprocess
import os
from .models import Video

@shared_task
def process_video(video_id):
    video = Video.objects.get(id=video_id)
    uploaded_video_path = video.upload_video_file.path
    output_video_name = f"{os.path.splitext(video.upload_video_file.name)[0]}_processed.mp4"
    output_video_path = os.path.join("processed_videos", output_video_name)

    # 모델 경로 수정
    model_path = os.path.abspath("models/ball.pt")

    try:
        # subprocess를 통해 run.py 실행
        subprocess.run(
            [
                "python",
                "run.py",
                "--model",
                model_path,  # 모델 경로 절대 경로로 설정
                "--video",
                uploaded_video_path,
                "--output", # 출력 경로 추가
                output_video_path,
                "--possession",  # possession 분석 활성화
                "--passes",  # 패스 분석 활성화
            ],
            check=True,
        )
        # Celery 작업 완료 후 DB에 출력 비디오 파일 경로 저장
        video.download_video_file = output_video_path
        video.save()
        return f"Video {video_id} processed successfully."
    except subprocess.CalledProcessError as e:
        raise Exception(f"Subprocess error: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")