import collections
from threading import Thread
import cv2
import time
import numpy as np
import sys
(width, height) = 640, 480


class VideoScreenshot(object):
    def __init__(self, src=0):
        # Create a VideoCapture object
        self.capture = cv2.VideoCapture(src)
        self.source_fps = self.capture.get(cv2.CAP_PROP_FPS)
        # Default resolutions of the frame are obtained (system dependent)
        self.frame_width = width
        self.frame_height = height
        self.size = self.frame_width, self.frame_height

        # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.update)
        self.thread.daemon = True
        self.thread.start()

        self.status = False
        self.frame = None
        self.fps = 0

        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def update(self):
        # Read the next frame from the stream in a different thread
        while True:
            if self.capture.isOpened():
                (self.status, frame) = self.capture.read()
                self.frame = cv2.resize(frame, self.size)

    def show_frame(self):
        # ID = 0
        # out = cv2.VideoWriter('output_blend.avi',
        #                       cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10,
        #                       (1900, 960))
        # Display frames in main program
        while True:
            if self.status:
                # start = time.time()
                # final = self.detect()
                # end = time.time()
                # self.fps = self.fps * 0.9 + 1 / (end - start) * 0.1
                # fps = "{:.2f}".format(self.fps)
                # final = cv2.putText(final, fps, (50, 50),
                #                     cv2.FONT_HERSHEY_SIMPLEX,
                #                     1, (255, 0, 0), 2, cv2.LINE_AA)
                # out.write(final)
                # cv2.imshow('result', final)
                img = self.frame.copy()
                sys.stdout.write(str(img))
                # sys.stdout.write(str(final))
                # sys.stdout.flush()
            # Press Q on keyboard to stop recording
            # key = cv2.waitKey(1)
            # if key == ord('q'):
            #     self.capture.release()
            #     cv2.destroyAllWindows()
            #     exit(1)

    def detect(self):
        img = self.frame.copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        return img


if __name__ == '__main__':
    video_stream_widget = VideoScreenshot(0)
    print(video_stream_widget.source_fps)
    time.sleep(1)
    video_stream_widget.show_frame()
