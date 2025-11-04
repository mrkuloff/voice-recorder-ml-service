import asyncio

from faststream.rabbit import RabbitBroker


RABBIT_MQ_URL = "amqp://rmuser:rmpassword@localhost:5672/"
broker = RabbitBroker(RABBIT_MQ_URL)

async def test_ml_service(audio: int):
    await broker.connect()
    await broker.publish(
        audio,
        queue="audio-transcription")

if __name__ == "__main__":
    audio_id = 1
    asyncio.run(test_ml_service(audio_id))