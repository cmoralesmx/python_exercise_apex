import logging
from pathlib import Path
from sys import argv
from os import mkdir
import csv

from db.PostgresDB import PostgresDB
from Video import VideoData, Cutter
# setup logging
my_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=my_format)


def main(filename: str):
    clips = []
    # cut video into 1-minute clips, save inside video_clips
    # each clip {i}thFrame.{ext}
    video_data = VideoData.VideoData(filename)

    # prepare_directories()

    cutter = Cutter.Cutter(video_data)
    tl = cutter.get_total_seconds()
    video_data.length = tl

    entries = cutter.split_video('video_clips', video_data.ext)

    with PostgresDB() as pg:
        for record in entries:
            pg.insert_record(
                record[0], 
                record[1],
                record[2],
                record[3])

    # create csv report
    write_csv(entries)

def prepare_directories():
    targets = ['video_clips', 'report']
    for target in targets:
        t = f'./{target}'
        mkdir(t)
        target_path = Path(t)
        if not (target_path.exists and target_path.is_dir):
            raise RuntimeError("Cannot create directory " + target)


def write_csv(entries: list[list[str]])->None:
    with open('./report/generated_video_files', 'wt') as csv_out:
        csv_writter = csv.writer(csv_out)
        csv_writter.writerows(entries)


if __name__ == '__main__':
    if len(argv) > 1:
        print(argv)
        main(argv[1])