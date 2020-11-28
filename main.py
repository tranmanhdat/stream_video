from threading import Thread
import cv2
import time
import sys
import numpy as np
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

        self.status = False
        self.frame = None
        self.fps = 0

        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")

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
                start = time.time()
                final = self.detect()
                end = time.time()
                self.fps = self.fps * 0.9 + 1 / (end - start) * 0.1
                fps = "{:.2f}".format(self.fps)
                final = cv2.putText(final, fps, (50, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    1, (255, 0, 0), 2, cv2.LINE_AA)
                # out.write(final)
                # cv2.imshow('result', final)
                sys.stdout.buffer.write(final.tobytes())
                # sys.stdout.flush()
            # Press Q on keyboard to stop recording
            # key = cv2.waitKey(1)
            # if key == ord('q'):
            #     self.capture.release()
            #     cv2.destroyAllWindows()
            #     exit(1)

    def detect(self):
        img = self.frame.copy()
        (h, w) = img.shape[:2]
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 0.007843,
                                     (300, 300), 127.5)
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
    # video_stream_widget = VideoScreenshot("rtsp://admin:hd2018vt@@27.67.55.46:554/profile2/media.smp")
    video_stream_widget = VideoScreenshot(
        "rtsp://operator:Abc@12345@192.168.1.64:554")
    # video_stream_widget = VideoScreenshot("rtsp://sla:1123456@117.6.121.13:554/axis-media/media.amp")
    # video_stream_widget = VideoScreenshot(0)
    print(video_stream_widget.source_fps)
    time.sleep(1)
    video_stream_widget.show_frame()
