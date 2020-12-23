from threading import Thread
import cv2
import time
import sys
import numpy as np
# (width, height) = 1920, 1080
# (width, height) = 640, 480
(width, height) = 1280, 720

class VideoScreenshot(object):
    def __init__(self, src=0):
        # Create a VideoCapture object
        self.capture = cv2.VideoCapture(src)
        # self.source_fps = self.capture.get(cv2.CAP_PROP_FPS)
        # Default resolutions of the frame are obtained (system dependent)
        self.frame_width = width
        self.frame_height = height
        self.size = self.frame_width, self.frame_height

        # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.update)
        self.thread.daemon = True
        self.thread.start()

        self.alpha = 0.95
        self.status = False
        self.frame = None
        self.fps_org = 0

    def update(self):
        # Read the next frame from the stream in a different thread
        while True:
            if self.capture.isOpened():
                start = time.time()
                (self.status, frame) = self.capture.read()
                self.frame = cv2.resize(frame, self.size)
                end = time.time()
                self.fps_org = self.fps_org * 0.95 + 1 / (end - start) * 0.05

    def show_frame(self):
        # Display frames in main program
        while True:
            if self.status:
                final = self.frame
                fps_org = "{:.2f}".format(self.fps_org)
                final = cv2.putText(final, "client"+fps_org, (50, 150),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    1, (255, 0, 0), 2, cv2.LINE_AA)
                cv2.imshow('result', final)
                key = cv2.waitKey(1)
                if key==ord("q"):
                    exit(0)
if __name__ == '__main__':
    video_stream_widget = VideoScreenshot("http://localhost:8090/facstream2.mjpeg")
    time.sleep(1)
    video_stream_widget.show_frame()
