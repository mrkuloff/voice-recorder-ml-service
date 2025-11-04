import os
import tempfile

import logging
from minio import Minio, S3Error

from data.config import S3_ENDPOINT, S3_ACCESS_KEY, S3_SECRET_KEY, S3_SECURE, S3_REGION

logger = logging.getLogger(__name__)

class DownloadService:
    """
    Сервис для скачивания аудио из MinIO во временный файл.
    """
    def __init__(self,
                 minio_endpoint: str = S3_ENDPOINT,
                 access_key: str = S3_ACCESS_KEY,
                 secret_key: str = S3_SECRET_KEY,
                 secure: bool = S3_SECURE,
                 region: str = S3_REGION):
        self.client = Minio(
            endpoint=minio_endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
            region=region
        )
    def download_temp_audio(self, bucket_name: str, object_name: str) -> str:
        if not self.client.bucket_exists(bucket_name):
            logger.error(f"Bucket '{bucket_name}' does not exist")

        # расширение
        _, ext = os.path.splitext(object_name)
        if not ext:
            ext = ".bin"

        # временный файл для дальнейшей работы
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
        tmp_path = tmp_file.name
        tmp_file.close()

        try:
            self.client.fget_object(
                bucket_name=bucket_name,
                object_name=object_name,
                file_path=tmp_path
            )
            logger.info(f"Downloaded '{object_name}' to temporary file: {tmp_path}")
            return tmp_path
        except S3Error as err:
            logger.error(f"S3 error: {err}")
            raise
        except Exception as ex:
            logger.error(f"General error: {ex}")
            raise

    @staticmethod
    def cleanup_temp_file(file_path: str) -> None:
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Deleted temporary file: {file_path}")
        except Exception as e:
            logger.error(f"Failed to delete temporary file {file_path}: {e}")
