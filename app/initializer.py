import logging

from os import mkdir
from pathlib import Path

from db.postgres import PostgresDB

# setup logging
my_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=my_format)


def initialize_app(filename: str) -> bool:
    """
    Initializes the DB, the output directories, the input video file
    """
    try:
        with PostgresDB() as pg:
            pg.initialize()

        check_video(filename)

        prepare_directories()

    except (Exception) as error:
        logging.error(f'ABORTING: {error}')
        return False
    return True


def prepare_directories() -> None:
    """Creates the basic directories needed"""
    targets = ['video_clips', 'report', 'processed']
    for target in targets:
        t = f'/app/data/{target}'
        try:
            mkdir(t)
            target_path = Path(t)
            if not (target_path.is_dir()):
                raise RuntimeError('Could not create directory ' + target)
            logging.debug(f'Directory created: {target}')
        except (Exception, FileExistsError) as error:
            raise RuntimeError(f'Could not create directory {target}: {error}')
    logging.debug('Basic directories created')


def check_video(filename) -> bool:
    target_video = Path(filename)
    if target_video.is_file():
        logging.debug(f'Input file found: {filename}')
        return True
    raise RuntimeError(f'Could not read input file: {filename}')
