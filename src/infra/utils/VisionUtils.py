import cv2
import numpy as np


class VisionUtils:
    @staticmethod
    def apply_area_filter(minimum_area, image):
        (
            componentsNumber,
            labeledImage,
            componentStats,
            componentCentroids,
        ) = cv2.connectedComponentsWithStats(image, connectivity=4)
        remainingComponentLabels = [
            i
            for i in range(1, componentsNumber)
            if componentStats[i][4] >= minimum_area
        ]
        filtered_image = np.where(
            np.isin(labeledImage, remainingComponentLabels) == True, 255, 0
        ).astype("uint8")

        return filtered_image
