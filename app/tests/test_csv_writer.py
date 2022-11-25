import pytest
from datetime import datetime

import csv_writer
from video.data import ClipData


@pytest.fixture
def clips():
    return [ClipData(0, '.mp4', 60, '/dummy')]


@pytest.fixture
def timestamps():
    return {0: datetime(2022, 12, 1)}


def test_file_not_exist_exception(clips, timestamps):
    with pytest.raises(FileNotFoundError):
        w = csv_writer.Writer('./dummy_path')
        w.write('my_video', clips, timestamps)
