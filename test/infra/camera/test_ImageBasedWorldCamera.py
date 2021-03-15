from unittest import TestCase

import cv2

from infra.camera.ImageBasedWorldCamera import ImageBasedWorldCamera


class TestImageBasedWorldCamera(TestCase):
    IMAGE_PATH = "resources/test/puck-detector-test-marker-3.jpg"

    def test_whenTakeWorldImage_thenReadImageFromResources(self):
        world_camera = ImageBasedWorldCamera(self.IMAGE_PATH)
        expected_image = cv2.imread(self.IMAGE_PATH)

        actual_image = world_camera.take_world_image()

        image_difference = cv2.subtract(expected_image, actual_image)
        self.assertFalse(image_difference.any())
