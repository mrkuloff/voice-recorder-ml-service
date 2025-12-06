import logging
import requests
from pydantic import PositiveInt

from data.config import BUSINESS_LOGIC_SERVICE, BUSINESS_LOGIC_API_KEY
from pydantic_model.model import SegmentsModel

logger = logging.getLogger(__name__)

class SendService:
    """
    Класс для отправки данных в основной сервис бизнес-логики проекта
    """

    def __init__(self,
                 backend_url: str = BUSINESS_LOGIC_SERVICE,
                 api_key: str = BUSINESS_LOGIC_API_KEY,
                 ):
        self.backend_url = backend_url.rstrip("/")
        self.api_key = api_key

    def _make_headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "X-API-Key": f"{self.api_key}"
        }

    def send_transcription(self,
                           record_id: PositiveInt,
                           segments: SegmentsModel):
        url = f"{self.backend_url}/records/{record_id}/transcribe"
        headers = self._make_headers()

        payload = {
            segments.model_dump()
        }

        logger.info(f"Request payload {payload}")

        response = requests.post(url, json=payload, headers=headers)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            logger.error(f"Failed to send transcription [{response.status_code}] : {response.text}")
        logger.info(f"Sent transcription for record {record_id}, "
                    f"server responded: {response.status_code}")