import os
import tempfile

import logging
from typing import Optional

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
    def download_temp_audio(self, bucket_name: str, record_id: int) -> Optional[str]:
        if not self.client.bucket_exists(bucket_name):
            logger.error(f"Bucket '{bucket_name}' does not exist")
        object_name = f"{record_id}.m4a"

        tmp_dir = tempfile.mkdtemp()
        tmp_path = os.path.join(tmp_dir, object_name)

        try:
            self.client.stat_object(bucket_name, object_name)
        except S3Error as err:
            logger.error(f"S3 error: {err}")
            return None

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
            return None
        except Exception as ex:
            logger.exception(f"General error: {ex}")
            return None

    @staticmethod
    def cleanup_temp_dir(dir_path: str) -> None:
        try:
            if dir_path and os.path.exists(dir_path):
                for root, dirs, files in os.walk(dir_path, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                os.rmdir(dir_path)
                logger.info(f"Deleted temporary directory: {dir_path}")
        except Exception as e:
            logger.error(f"Failed to delete temporary directory {dir_path}: {e}")
