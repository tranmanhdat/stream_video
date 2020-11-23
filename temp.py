import cv2

if __name__ == '__main__':
    capture = cv2.VideoCapture("http://localhost:8090/facstream.mjpeg")
    print(capture.get(cv2.CAP_PROP_FPS))
    last_frame = None
    while True:
        ret, frame = capture.read()
