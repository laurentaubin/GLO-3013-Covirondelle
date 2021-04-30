from unittest import TestCase

import cv2

from infra.camera.ImageBasedEmbeddedCamera import ImageBasedEmbeddedCamera


class TestImageEmbeddedCamera(TestCase):
    IMAGE_PATH = "resources/test/test_embedded_camera.jpg"

    def test_whenTakeEmbeddedImage_thenReadImageFromResources(self):
        embedded_camera = ImageBasedEmbeddedCamera(self.IMAGE_PATH)
        expected_image = cv2.imread(self.IMAGE_PATH)

        actual_image = embedded_camera.take_image()

        image_difference = cv2.subtract(expected_image, actual_image)
        self.assertFalse(image_difference.any())
