# import the necessary packages
import os

from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import argparse
import imutils
import time
import dlib
import cv2

from blink_detector import BlinkDetector
from datalogger import DataLogger
from eye_metrics import eye_aspect_ratio, AreaDistanceRatio

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", default="shape_predictor_68_face_landmarks.dat",
                help="path to facial landmark predictor")
ap.add_argument("-v", "--video", type=str, default="camera",
                help="path to input video file")
ap.add_argument("-g", "--graph",  action='store_true',
                help="show graph")
ap.add_argument("-o", "--output-file", type=str, default=None,
                help="the output file where collected metrics will be stored")


class FPSCounter:
    ''' 
    Frame counter class used to calculate fps (frame per second)
    live
    '''
    def __init__(self):
        self._last_tick_time = time.time()
        self._fps = 0

    def tick(self):
        ''' This function should be called on every frame 
        it will update its interal fps attribute according the 
        time difference to previous frame'''
        now = time.time()
        dt = now - self._last_tick_time
        self._fps = round(1 / dt)
        self._last_tick_time = now
        return self._fps

    def get_fps(self):
        ''' Returns the fps (frame rate)'''
        return self._fps


def main():
    args = vars(ap.parse_args())

    # create frame counter
    fps_counter = FPSCounter()

    # total number of blinks
    TOTAL = 0

    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    print("[INFO] loading facial landmark predictor...")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(args["shape_predictor"])

    # grab the indexes of the facial landmarks for the left and
    # right eye, respectively
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    # start the video stream thread
    print("[INFO] starting video stream thread...")
    print("[INFO] print q to quit...")
    if args['video'] == "camera":
        vs = VideoStream(src=0).start()
        vs.stream.set(cv2.CAP_PROP_FPS, 15)
        fileStream = False
    else:
        vs = FileVideoStream(args["video"]).start()
        fileStream = True
        fps = vs.stream.get(cv2.CAP_PROP_FPS)

    # create dataloggers
    datalogger = DataLogger(columns=['ear', 'adr'])

    # blink detector
    blink_detector = BlinkDetector(time_window=5,
                                   plot=args['graph'],
                                   frame_delay=10)

    # loop over frames from the video stream
    frame_cnt = 0
    INIT_TIME = None
    while True:
        # if this is a file video stream, then we need to check if
        # there any more frames left in the buffer to process
        if fileStream and not vs.more():
            break

        # get timestamp
        if fileStream:
            timestamp = frame_cnt / fps
        else:
            if INIT_TIME is None:
                INIT_TIME = time.time()
            timestamp = time.time() - INIT_TIME
            fps = fps_counter.tick()

        # get the new frame
        frame = vs.read()
        frame_cnt += 1
        if frame is None:
            break

        frame = imutils.resize(frame, width=450)
        # it, and convert it to grayscale channels)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect faces in the grayscale frame
        rects = detector(gray, 0)

        # loop over the face detections
        for rect in rects:
            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy
            # array

            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            # extract the left and right eye coordinates, then use the
            # coordinates to compute the eye aspect ratio for both eyes
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)

            # compute the area-over-distance metric
            adr = AreaDistanceRatio.compute(leftEye, rightEye)
            # log ADR
            datalogger.log(adr, 'adr', timestamp)

            # average the eye aspect ratio together for both eyes
            ear = (leftEAR + rightEAR) / 2.0
            # log EAR
            datalogger.log(ear, 'ear', timestamp)

            # compute the convex hull for the left and right eye, then
            # visualize each of the eyes
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

            # send new data to blink detector and check if it detected new blinks
            blink_detector.send(adr, timestamp)
            blink = blink_detector.get_blink()
            if blink is not None:
                blink_time, blink_dur = blink
                TOTAL += 1
                print(f"[BLINK] time: {blink_time:.2f}  dur: {blink_dur:.2f}")

            # draw the total number of blinks on the frame along with
            # the computed eye aspect ratio for the frame
            cv2.putText(frame, "Blinks: {}".format(TOTAL), (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, "ADR: {:.2f}".format(ear), (300, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, "FPS: {:.2f}".format(fps), (300, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # show the frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

    # save datafile
    output_file = args['output_file']
    if output_file == 'ask':
        output_file = input("Enter filename to save: ")
    if output_file is not None:
        datalogger.save(output_file)

    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()


if __name__ == '__main__':
    main()
