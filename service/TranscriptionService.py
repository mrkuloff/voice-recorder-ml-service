import logging

from faster_whisper import WhisperModel

from pydantic_model.model import SegmentsModel, TranscriptionModel

logger = logging.getLogger(__name__)


class TranscriptionService:
    """
    Сервис для транскрибации аудиофайлов
    """

    def __init__(self,
                 model_size: str = "medium",
                 device: str = "cpu",
                 beam_size: int = 5,
                 language: str = "ru"):
        self.model = WhisperModel(model_size, device=device)
        self.beam_size = beam_size
        self.language = language

        logger.info(f"Loaded Whisper model '{model_size}' on {device}")

    def transcribe(self, file_path: str) -> SegmentsModel:
        logger.info(f"Starting transcription for {file_path}")

        try:
            segments, _ = self.model.transcribe(
                file_path,
                language=self.language,
                condition_on_previous_text=False,
                beam_size=self.beam_size
            )

            result_segments: list[TranscriptionModel] = []

            for segment in segments:
                logger.debug(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
                result_segments.append(
                    TranscriptionModel(
                        start=int(segment.start),
                        end=int(segment.end),
                        text=segment.text.strip()
                    )
                )

            logger.info(f"Transcription completed for {file_path}. "
                        f"Total segments: {len(result_segments)}")

            return SegmentsModel(segments=result_segments)

        except Exception as e:
            logger.exception(f"Error while transcribing file {file_path}: {e}")
            raise
