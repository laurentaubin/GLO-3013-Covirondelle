from unittest import TestCase
from unittest.mock import Mock

from service.vision.VisionService import VisionService


class TestVisionService(TestCase):

    image = 'an image'

    def setUp(self):
        self.detector = Mock()
        self.visionService = VisionService(self.detector)

    def test_givenAnImage_whenDetect_thenDetectorDetectItemsOnImage(self):
        self.visionService.detect(self.image)

        self.detector.detect.assert_called_with(self.image)
