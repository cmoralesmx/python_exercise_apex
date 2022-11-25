import cv2
import logging
from .data import VideoData, ClipData

# setup logging
my_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=my_format)


class Cutter:
    """
    This video segmenter depends on OpenCV for processing the video.
    """

    def __init__(self, video: VideoData) -> None:
        """
        The video process needs basic data about the source video,
        such as the number of Frames per Second, the estimated total frames
        and the dimmensions of the video stream
        """
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
        """
        Single threaded implementation of a video splitter task

        """
        clips = []

        logging.debug('Single threaded')

        # The video writer must be set up per file written
        cccc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        out = cv2.VideoWriter()

        first_frame, frame_idx, clip_number = 0, 0, 1
        # A hard limit for the frames to write in the current output file
        upper_limit = self.fps * 60 * clip_number

        clip = ClipData(frame_idx, ext)
        out_file = clip.get_output_file_name()
        logging.debug(f'{out_file=}')

        # Open the target video file for writing
        out.open(out_file, cccc, self.fps, (self.width, self.height), True)
        try:
            while True:
                # copy frame-by-frame from the source to the target files
                ret, frame = self.cap.read()
                if not ret:
                    break
                out.write(frame)
                frame_idx += 1

                # keep writing the current clip until reaching the upper limit
                if frame_idx < upper_limit:
                    continue
                # Once the limit is reached, release the current target
                out.release()

                # The lenght of the clip in seconds: t = t1 - t0
                # Which means: the frames written to the recently closed file
                # times the FPS
                d = ((frame_idx - 1) - first_frame) / self.fps
                logging.debug(
                    f'Done with clip {frame_idx-1} {first_frame} {d}'
                )
                clip.duration = d
                clips.append(clip)

                # Initialize the parameters for the next target file
                first_frame = frame_idx

                clip_number += 1
                upper_limit = self.fps * 60 * clip_number

                clip = ClipData(frame_idx, ext)
                out_file = clip.get_output_file_name()
                logging.debug(f"{out_file=}")

                # Open the next target file for writing
                out.open(
                    out_file, cccc, self.fps, (self.width, self.height), True
                )
        except Exception as error:
            # Respose the resurces in case of an error
            self.cap.release()
            out.release()
            logging.error(error)

        # Release the resources still in use after a successful execution
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
