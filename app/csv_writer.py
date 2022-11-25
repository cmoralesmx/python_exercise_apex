import csv
import logging
from os import path

from video.data import ClipData

# setup logging
my_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=my_format)


class Writer:
    def __init__(self, base_path: str = '/app/data/report'):
        self.base_path = base_path

    def get_target_file(self) -> str:
        return path.join(self.base_path, 'generated_video_file')

    def write(
        self, video_name: str, clips: list[ClipData], timestamps: dict
    ) -> None:
        with open(self.get_target_file(), 'wt') as csv_out:
            csv_writter = csv.writer(csv_out)
            csv_writter.writerows(
                [
                    [
                        video_name,
                        record.get_clip_name(),
                        record.extension,
                        record.duration,
                        record.location,
                        timestamps[record.first_frame],
                    ]
                    for record in clips
                ]
            )
