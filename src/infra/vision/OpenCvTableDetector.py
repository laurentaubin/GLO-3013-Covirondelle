import cv2

from domain.vision.ITableDetector import ITableDetector


# https://docs.opencv.org/3.1.0/dd/d49/tutorial_py_contour_features.html
# https://docs.opencv.org/master/d7/d4d/tutorial_py_thresholding.html
# https://stackoverflow.com/questions/37177811/crop-rectangle-returned-by-minarearect-opencv-python
class OpenCvTableDetector(ITableDetector):
    MARGIN = 150

    def __init__(self):
        pass

    def crop_table(self, image):
        contour = self._get_table_contour(image)

        bounding_rectangle = cv2.minAreaRect(contour)
        box = cv2.boxPoints(bounding_rectangle)

        bounding_rectangle_width = bounding_rectangle[1][0] + self.MARGIN / 2
        bouding_rectangle_height = bounding_rectangle[1][1] + self.MARGIN / 2

        box = self._add_margin(box, self.MARGIN)

        Xs = [i[0] for i in box]
        Ys = [i[1] for i in box]
        x1 = min(Xs)
        x2 = max(Xs)
        y1 = min(Ys)
        y2 = max(Ys)

        angle = bounding_rectangle[2]

        center = ((x1 + x2) / 2, (y1 + y2) / 2)
        size = (int(x2 - x1), int(y2 - y1))
        rotation_matrix = cv2.getRotationMatrix2D(
            (size[0] / 2, size[1] / 2), angle, 1.0
        )
        cropped = cv2.getRectSubPix(image, size, center)
        cropped = cv2.warpAffine(cropped, rotation_matrix, size)
        cropped = cv2.getRectSubPix(
            cropped,
            (int(bounding_rectangle_width), int(bouding_rectangle_height)),
            (size[0] / 2, size[1] / 2),
        )
        return cropped

    def _get_table_contour(self, image):
        grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(grey_image, (5, 5), 0)
        ret, threshold = cv2.threshold(
            blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        contours, hierarchy = cv2.findContours(
            threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )
        approximate_contours = []
        for contour in contours:
            epsilon = 0.1 * cv2.arcLength(contour, True)
            approximate_contours.append(cv2.approxPolyDP(contour, epsilon, True))
        return max(approximate_contours, key=cv2.contourArea)

    def _add_margin(self, box, margin):
        box[0][0] = box[0][0] - margin
        box[0][1] = box[0][1] + margin

        box[1][0] = box[1][0] - margin
        box[1][1] = box[1][1] - margin

        box[2][0] = box[2][0] + margin
        box[2][1] = box[2][1] - margin

        box[3][0] = box[3][0] + margin
        box[3][1] = box[3][1] + margin
        return box
