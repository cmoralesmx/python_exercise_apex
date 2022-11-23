import cv2
import logging
import subprocess as sp
import multiprocessing as mp
from pathlib import Path

from main import VideoData

# setup logging
my_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=my_format)


class Cutter:
    def __init__(self, video:VideoData)-> None:
        self.cap = cv2.VideoCapture(video.filename)
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def get_total_seconds(self) -> int:
        self.seconds = self.frame_count / self.fps
        print(f"Seconds estimated {self.seconds}")
            
        return self.seconds

    def split_video(self, sub, ext)->list[int]:
        """Split the video in 1-minute intervals, return total length"""
        return self.single_threaded(sub, ext)


    def single_threaded(self, sub, ext)->list[int]:
        init_frames = []

        logging.debug('Single threaded')
        cccc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        out = cv2.VideoWriter()

        first_frame, frame_idx, clip_number = 0, 0, 1

        out_file = f'./{sub}/{frame_idx}thFrame{ext}'
        logging.debug(f'{out_file=}')

        out.open(out_file, cccc, self.fps, (self.width, self.height), True)
        try:
            while self.cap.isOpened():
                ret, frame = self.read()
                if not ret:
                    break
                out.write(frame)

                frame_idx += 1

                # we are wtill sriting the current clip
                if frame_idx < upper_limit:
                    continue
                # otherwise, we must start the next clip
                out.release()
                logging.out('Done with one clip')
                
                # duration = t1 - t0
                d = (frame_idx - 1) * self.fps - first_frame * self.fps
                init_frames.append([f'{first_frame}thFrame', f'{ext}', d, f'./{sub}'])
                first_frame = frame_idx

                clip_number += 1
                upper_limit = self.fps * 60 * clip_number
                out_file = f'./{sub}/{frame_idx}thFrame{ext}'
                logging.debug(f'{out_file=}')

                out.open(out_file, cccc, self.fps, (self.width, self.height), True)
        except:
            self.cap.release()
            out.release()

        self.cap.release()
        out.release()

        logging.debug('Done splitting the video')
        return init_frames