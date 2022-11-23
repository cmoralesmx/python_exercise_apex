import cv2
import time
import subprocess as sp
import multiprocessing as mp
from pathlib import Path

from main import VideoData


class Cutter:
    def __init_(self, video:VideoData)-> None:
        self.cap = cv2.VideoCapture(video.original_path)
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))

    def get_total_legth(self) -> int:
        frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 1)
        last = int(self.cap.get(cv2.CAP_PROP_POS_MSEC))
        self.cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)
        return last

    def split_video()->int:
        """Split the video in 1-minute intervals, return total length"""
        out = cv2.VideoWriter()
