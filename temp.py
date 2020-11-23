import cv2

if __name__ == '__main__':
    capture = cv2.VideoCapture(0)
    while True:
        status, frame = capture.read()
        frame = cv2.resize(frame, (640, 480))
        if status:
            cv2.imshow("image", frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            capture.release()
            cv2.destroyAllWindows()
            exit(1)