import logging
from pathlib import Path
from sys import argv
from os import mkdir

from db.PostgresDB import PostgresDB
from Video.Cutter import Cutter
from Video.VideoData import VideoData


# setup logging
my_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=my_format)


def main(filename: str):
    clips = []
    # cut video into 1-minute clips, save inside video_clips
    # each clip {i}thFrame.{ext}
    video_data = VideoData(filename)

    prepare_directories()

    cutter = Cutter(video_data)
    tl = cutter.get_total_legth()
    video_data.length = tl

    with PostgresDB() as pg:
        pg.insert_record(
            video_data.name, 
            video_data.ext,
            video_data.length,
            video_data.path)

    # create csv report

def prepare_directories():
    targets = ['video_clips', 'report']
    for target in targets:
        t = f'./{target}'
        mkdir(t)
        target_path = Path(t)
        if not (target_path.exists and target_path.is_dir):
            raise RuntimeError("Cannot create directory " + target)




if __name__ == '__main__':
    if len(argv) > 1:
        print(argv)
        main(argv[1])