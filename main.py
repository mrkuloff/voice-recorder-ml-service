import logging

from faststream import FastStream
from faststream.rabbit import RabbitBroker
from pydantic import PositiveInt

from data.config import RABBIT_MQ_URL
from service.AudioDownloadTranscriptionService import AudioDownloadTranscriptionService

broker = RabbitBroker(RABBIT_MQ_URL)
app = FastStream(broker)

logging.basicConfig(level=logging.INFO)

@broker.subscriber("audio-transcription")
async def handle(record_id: PositiveInt):
   audio_transcribe = AudioDownloadTranscriptionService()
   await audio_transcribe.record(record_id=record_id)