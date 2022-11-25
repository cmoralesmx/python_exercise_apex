import csv
import logging

from sys import argv

from db.postgres import PostgresDB
from initializer import initialize_app
from video.cutter import Cutter
from video.data import VideoData, ClipData

# setup logging
my_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=my_format)


def main(filename: str):
    if initialize_app(filename):

        video_data = VideoData(filename)

        video_cutter = Cutter(video_data)
        tl = video_cutter.get_total_seconds()
        video_data.length = tl

        clips = video_cutter.split_video(video_data.ext)
        tstamps = {}

        with PostgresDB() as pg:
            for record in clips:
                tstamps[record.first_frame] = pg.insert_record(
                    video_data.name,
                    record.get_clip_name(),
                    record.extension,
                    record.duration,
                    record.location,
                )
        # create csv report
        write_csv(
            [
                [
                    video_data.name,
                    record.get_clip_name(),
                    record.extension,
                    record.duration,
                    record.location,
                    tstamps[record.first_frame],
                ]
                for record in clips
            ]
        )


def write_csv(entries: list[list[str]]) -> None:
    with open('/app/data/report/generated_video_files', 'wt') as csv_out:
        csv_writter = csv.writer(csv_out)
        csv_writter.writerows(entries)


if __name__ == '__main__':
    if len(argv) > 1:
        print(argv)
        main(argv[1])
