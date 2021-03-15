import cv2

from domain.camera.IWorldCamera import IWorldCamera


class ImageBasedWorldCamera(IWorldCamera):
    def __init__(self, image_path: str):
        self._image_path = image_path

    def take_world_image(self):
        return cv2.imread(self._image_path)
