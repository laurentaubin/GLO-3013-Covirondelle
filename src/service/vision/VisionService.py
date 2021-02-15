from domain.vision.IDetector import IDetector


class VisionService:
    def __init__(self, detector: IDetector):
        self.detector = detector

    def detect(self, image):

        self.detector.detect(image)
