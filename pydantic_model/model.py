from pydantic import BaseModel


class TranscriptionModel(BaseModel):
    start: float
    end: float
    text: str

class SegmentsModel(BaseModel):
    segments: list[TranscriptionModel]