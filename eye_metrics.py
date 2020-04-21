from scipy.spatial import distance as dist
import math

def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])

    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # return the eye aspect ratio
    return ear


class AreaDistanceRatio():
    @staticmethod
    def compute(leftEye, rightEye):
        leftEyeArea = AreaDistanceRatio.eye_area(leftEye)
        rightEyeArea = AreaDistanceRatio.eye_area(rightEye)
        leftEyeCenter = AreaDistanceRatio.eye_center(leftEye)
        rightEyeCenter = AreaDistanceRatio.eye_center(rightEye)
        eyeDistance = dist.euclidean(leftEyeCenter, rightEyeCenter)
        eyeAvgArea = (leftEyeArea + rightEyeArea) / 2
        areaOverDist = math.sqrt(eyeAvgArea) / eyeDistance
        return areaOverDist

    @staticmethod
    def polygon_area(corners):
        n = len(corners)  # of corners
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += corners[i][0] * corners[j][1]
            area -= corners[j][0] * corners[i][1]
        area = abs(area) / 2.0
        return area

    @staticmethod
    def eye_area(eye):
        return AreaDistanceRatio.polygon_area(eye)

    @staticmethod
    def eye_center(eye):
        # get leftmost and rightmost point
        # compute the center of these two points
        xmid = (eye[0][0] + eye[3][0]) / 2
        ymid = (eye[0][1] + eye[3][1]) / 2
        return (xmid, ymid)

