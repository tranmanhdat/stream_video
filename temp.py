import time

import cv2

if __name__ == '__main__':
    capture = cv2.VideoCapture("http://localhost:8090/facstream.mjpeg") # local test
    # capture = cv2.VideoCapture("http://operator:Abc@12345@27.72.105.10:8933/Streaming/channels/101/httpPreview")
    # capture = cv2.VideoCapture("http://210.148.114.53/-wvhttp-01-/GetOneShot?image_size=640x480&frame_count=1000000000")
    # capture = cv2.VideoCapture("rtsp://admin:hd2018vt@@27.67.55.46:554/profile2/media.smp") #viettel
    # capture = cv2.VideoCapture(0)
    print(capture.get(cv2.CAP_PROP_FPS))
    capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    last_frame = None
    start = time.time()
    fps = 0
    while True:
        ret, frame = capture.read()
        # print(frame.shape)
        if ret:
            end = time.time()
            fps = 0.8*fps + 0.2*1/(end-start) if fps>0 else 1/(end-start)
            start = end
            print(fps)
            cv2.imshow("img", frame)
            key = cv2.waitKey(1)
            if key == ord('q'):
                capture.release()
                cv2.destroyAllWindows()
                exit(1)