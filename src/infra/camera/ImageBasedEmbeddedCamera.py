import cv2

from domain.camera.IEmbeddedCamera import IEmbeddedCamera


class ImageBasedEmbeddedCamera(IEmbeddedCamera):
    def __init__(self, image_path: str):
        self._image_path = image_path

    def take_image(self):
        return cv2.imread(self._image_path)
