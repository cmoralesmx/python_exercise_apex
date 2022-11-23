
from pathlib import Path


class VideoData:
    def __init__(self, filename: str):
        self.filename = filename
        self.original_path = Path(filename)
        self.name = self.original_path.stem
        self.ext = self.original_path.suffix
        self.path = filename[: -(len(self.ext) + len(self.name))]
    
    def __str__(self) -> str:
        return f"{self.name=}, {self.ext=}, {self.path=}"

    
    def set_total_length(self, length: int) -> None:
        self.length = length