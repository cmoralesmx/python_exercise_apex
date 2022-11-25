import pytest

import initializer


def test_check_video_passes_with_RuntimeError():
    with pytest.raises(RuntimeError):
        initializer.check_video('dummy')

