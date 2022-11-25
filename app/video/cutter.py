import cv2
import logging
from .data import VideoData, ClipData

# setup logging
my_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=my_format)


class Cutter:
    def __init__(self, video: VideoData) -> None:
        self.cap = cv2.VideoCapture(video.filename)
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def get_total_seconds(self) -> int:
        """
        Returns the length of the video in seconds.
        This value is computed by dividing the total frames by the
        frames per second
        """
        self.seconds = self.frame_count / self.fps
        print(f"Seconds estimated {self.seconds}")

        return self.seconds

    def split_video(self, ext) -> list[ClipData]:
        """Split the video in 1-minute intervals"""
        return self.single_threaded(ext)

    def single_threaded(self, ext) -> list[ClipData]:
        clips = []

        logging.debug('Single threaded')
        cccc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        out = cv2.VideoWriter()

        first_frame, frame_idx, clip_number = 0, 0, 1
        upper_limit = self.fps * 60 * clip_number

        clip = ClipData(frame_idx, ext)
        out_file = clip.get_output_file_name()
        logging.debug(f'{out_file=}')

        out.open(out_file, cccc, self.fps, (self.width, self.height), True)
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    break
                out.write(frame)
                frame_idx += 1

                # we are still writing the current clip
                if frame_idx < upper_limit:
                    continue
                # otherwise, we must start the next clip
                out.release()

                # duration = t1 - t0
                d = ((frame_idx - 1) - first_frame) / self.fps
                logging.debug(
                    f'Done with clip {frame_idx-1} {first_frame} {d}'
                )
                clip.duration = d
                clips.append(clip)
                first_frame = frame_idx

                clip_number += 1
                upper_limit = self.fps * 60 * clip_number
                clip = ClipData(frame_idx, ext)
                out_file = clip.get_output_file_name()
                logging.debug(f"{out_file=}")

                out.open(
                    out_file, cccc, self.fps, (self.width, self.height), True
                )
        except Exception as error:
            self.cap.release()
            out.release()
            logging.error(error)

        self.cap.release()
        out.release()

        d = ((frame_idx - 1) - first_frame) / self.fps
        logging.debug(
            f'Done with the last clip {frame_idx-1} {first_frame} {d}'
        )
        clip.duration = d
        clips.append(clip)
        logging.debug('Done splitting the video')
        return clips
