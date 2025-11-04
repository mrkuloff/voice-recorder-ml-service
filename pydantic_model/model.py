from pydantic import BaseModel


class TranscriptionModel(BaseModel):
    start: int
    end: int
    text: str

class SegmentsModel(BaseModel):
    segments: list[TranscriptionModel]