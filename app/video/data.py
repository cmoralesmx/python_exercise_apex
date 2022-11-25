from dataclasses import dataclass
from pathlib import Path


@dataclass
class VideoData:
    filename: str

    def __post_init__(self):
        self.original_path = Path(self.filename)
        self.name = self.original_path.stem
        self.ext = self.original_path.suffix
        self.path = self.filename[: -(len(self.ext) + len(self.name))]

    def __str__(self) -> str:
        return f'{self.name=}, {self.ext=}, {self.path=}'

    def set_total_length(self, length: int) -> None:
        self.length = length


@dataclass
class ClipData:
    first_frame: int
    extension: str
    duration: float = 0
    location: str = '/app/data/video_clips/'

    def get_clip_name(self):
        return f'{self.first_frame}thFrame'

    def get_output_file_name(self):
        return f'{self.location}{self.get_clip_name()}{self.extension}'
