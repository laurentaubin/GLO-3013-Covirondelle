from domain.StartingZone import StartingZone


class ICornerDetector:
    def detect_starting_zone(self, image) -> StartingZone:
        pass
