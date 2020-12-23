import argparse
from threading import Thread
import cv2
import time
import sys
import numpy as np
# (width, height) = 1920, 1080
(width, height) = 640, 480
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

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

        self.alpha = 0.95
        self.status = False
        self.frame = None
        self.fps_org = 0
        self.fps = 0
        self.net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")

    def update(self):
        # Read the next frame from the stream in a different thread
        while True:
            if self.capture.isOpened():
                start = time.time()
                (self.status, frame) = self.capture.read()
                self.frame = cv2.resize(frame, self.size)
                end = time.time()
                self.fps_org = self.fps_org * self.alpha + 1 / (end - start) * (1-self.alpha)

    def show_frame(self):
        # Display frames in main program
        while True:
            if self.status:
                start = time.time()
                final = self.detect()
                end = time.time()
                self.fps = self.fps * self.alpha + 1 / (end - start) * (1-self.alpha)
                fps = "{:.2f}".format(self.fps)
                fps_org = "{:.2f}".format(self.fps_org)
                final = cv2.putText(final, fps, (50, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    1, (255, 0, 0), 2, cv2.LINE_AA)
                final = cv2.putText(final, fps_org, (150, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    1, (255, 0, 0), 2, cv2.LINE_AA)
                # out.write(final)
                # cv2.imshow('result', final)
                sys.stdout.buffer.write(final.tobytes())
                # sys.stdout.flush()

    def detect(self):
        img = self.frame.copy()
        (h, w) = img.shape[:2]
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 0.007843,
                                     (300, 300), 127.5)
        # blobs = cv2.dnn.blobFromImages(img)/
        self.net.setInput(blob)
        detections = self.net.forward()

        # loop over the detections
        for i in np.arange(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with
            # the prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections by ensuring the `confidence` is
            # greater than the minimum confidence
            if confidence > 0.3:
                # extract the index of the class label from the
                # `detections`, then compute the (x, y)-coordinates of
                # the bounding box for the object
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # draw the prediction on the frame
                label = "{}: {:.2f}%".format(CLASSES[idx],
                                             confidence * 100)
                cv2.rectangle(img, (startX, startY), (endX, endY),
                              COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(img, label, (startX, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
        return img


if __name__ == '__main__':
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('--rtsp_link', '-rtsp', action='store', type=str,
                           required=True)
    args = my_parser.parse_args()
    rtsp = args.rtsp_link
    video_stream_widget = VideoScreenshot(rtsp)
    # video_stream_widget = VideoScreenshot(
    #     "rtsp://operator:Abc@12345@192.168.1.64:554")
    # video_stream_widget = VideoScreenshot("rtsp://sla:1123456@117.6.121.13:554/axis-media/media.amp")
    # video_stream_widget = VideoScreenshot(0)
    print(video_stream_widget.source_fps)
    time.sleep(1)
    video_stream_widget.show_frame()
