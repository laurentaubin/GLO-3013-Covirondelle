import cv2

from domain.vision.IPuckCenterDetector import IPuckCenterDetector


class OpenCvPuckCenterDetector(IPuckCenterDetector):
    def detect(self, image):

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred_img = cv2.medianBlur(gray, 5)

        circles = cv2.HoughCircles(
            blurred_img,
            cv2.HOUGH_GRADIENT,
            1,
            26,
            param1=30,
            param2=30,
            minRadius=15,
            maxRadius=35,
        )

        centers_list = []
        for circle in circles[0, :]:

            center_coordinates = [circle[1], circle[2]]
            centers_list.append(center_coordinates)

        return centers_list
