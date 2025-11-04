from data.config import S3_ENDPOINT, S3_ACCESS_KEY, S3_SECRET_KEY, S3_SECURE, S3_REGION, BUSINESS_LOGIC_SERVICE, \
    BUSINESS_LOGIC_API_KEY, WHISPER_MODEL_NAME, S3_BUCKET
from service.DownloadService import DownloadService
from service.SendService import SendService
from service.TranscriptionService import TranscriptionService


class AudioDownloadTranscriptionService:
    def __init__(self):
        self.download_service = DownloadService(
            minio_endpoint=S3_ENDPOINT,
            access_key=S3_ACCESS_KEY,
            secret_key=S3_SECRET_KEY,
            secure=S3_SECURE,
            region=S3_REGION
        )
        self.send_service = SendService(
            backend_url=BUSINESS_LOGIC_SERVICE,
            api_key=BUSINESS_LOGIC_API_KEY
        )
        self.transcription_service = TranscriptionService()
        self.bucket_name = S3_BUCKET

    def record(self,
               record_id: int):
        temp_path = None
        object_name = str(record_id)
        try:
            temp_path = self.download_service.download_temp_audio(self.bucket_name, object_name)
            segments = self.transcription_service.transcribe(temp_path)
            self.send_service.send_transcription(record_id, segments)
        finally:
            if temp_path:
                self.download_service.cleanup_temp_file(temp_path)
