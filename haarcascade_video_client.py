import cv2
import sys
import time

from detector import FaceDetector
from utils import annotate_image


def run(feed):
    cascPath = "./env/lib/python3.6/site-packages/cv2/data/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)

    if feed is None:
        # From webcam
        cap = cv2.VideoCapture(0)
    else:
        cap = cv2.VideoCapture(feed)

    # Get current width of frame
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float
    # Get current height of frame
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) # float
    fps = cap.get(cv2.CAP_PROP_FPS) # float


    # Define the codec and create VideoWriter object
    # fourcc = cv2.Video.CV_FOURCC(*'X264')
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter("output.avi",fourcc, fps, (int(width),int(height)))

    now = time.time()
    while(cap.isOpened()):
        now = time.time()

        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        now = time.time()

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        out.write(frame)

        # Display the resulting frame
        # cv2.imshow('frame', ann_frame)
        print("FPS: {:0.2f}".format(1 / (time.time() - now)))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    feed = None if len(sys.argv) == 1 else sys.argv[1]
    run(feed)
