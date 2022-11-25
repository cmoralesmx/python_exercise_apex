import csv
import logging

from video.data import ClipData

# setup logging
my_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=my_format)


def write(video_name: str, clips: list[ClipData], timestamps: dict) -> None:
    with open('/app/data/report/generated_video_files', 'wt') as csv_out:
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
