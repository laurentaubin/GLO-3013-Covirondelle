import time
from unittest.mock import MagicMock

import cv2
import serial

from config.config import (
    ROBOT_MAXIMUM_SPEED,
    SERVOING_CONSTANT,
    BASE_COMMAND_DURATION,
    STM_PORT_NAME,
    STM_BAUD_RATE,
    EMBEDDED_CAMERA_IMAGE_SIZE,
)
from domain.Position import Position
from domain.alignment.OhmmeterAlignmentCorrector import OhmmeterAlignmentCorrector
from domain.camera.IEmbeddedCamera import IEmbeddedCamera
from domain.movement.Direction import Direction
from domain.movement.MovementCommandFactory import MovementCommandFactory
from infra.motor_controller.StmMotorController import StmMotorController
from infra.vision.OpenCvStartingZoneLineDetector import OpenCvStartingZoneLineDetector
from service.movement.MovementService import MovementService
from service.vision.VisionService import VisionService


class OpenCvEmbeddedCamera(IEmbeddedCamera):
    def __init__(
        self,
        camera_index: int,
    ):
        self._camera_index = camera_index
        self._capture = None
        self._open_capture()

    def take_image(self):
        return self._get_camera_frame()

    def _get_camera_frame(self):
        opened_successfully, current_frame = self._capture.read()
        return current_frame

    def _open_capture(self):
        self._capture = cv2.VideoCapture(self._camera_index)
        self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, EMBEDDED_CAMERA_IMAGE_SIZE[0])
        self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, EMBEDDED_CAMERA_IMAGE_SIZE[1])
        self._capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    def _close_capture(self):
        self._capture.release()


if __name__ == "__main__":
    movement_command_factory = MovementCommandFactory(
        ROBOT_MAXIMUM_SPEED,
        SERVOING_CONSTANT,
        BASE_COMMAND_DURATION,
    )
    motor_controller = StmMotorController(
        serial.Serial(port=STM_PORT_NAME, baudrate=STM_BAUD_RATE)
    )
    camera = OpenCvEmbeddedCamera(0)

    vision_service = VisionService(camera, MagicMock())

    ALIGNED_OHMMETER_HORIZONTAL_POSITION = 349
    OHMMETER_ALIGNMENT_THRESHOLD = 10
    movement_service = MovementService(movement_command_factory, motor_controller)
    starting_zone_line_detector = OpenCvStartingZoneLineDetector()

    ohmmeter_alignment_corrector = OhmmeterAlignmentCorrector(
        Position(ALIGNED_OHMMETER_HORIZONTAL_POSITION, 0),
        OHMMETER_ALIGNMENT_THRESHOLD,
        starting_zone_line_detector,
    )

    while True:
        instruction = input("ready? (y/n)")
        if instruction == "y":
            break

    current_image = vision_service.take_image()
    adjustment_movement_command = (
        ohmmeter_alignment_corrector.calculate_horizontal_correction(current_image)
    )

    if adjustment_movement_command.get_direction() == Direction.STOP:
        print("align")
    else:
        movement_service.execute_movement_command(adjustment_movement_command)
        while adjustment_movement_command.get_direction() != Direction.STOP:
            time.sleep(0.5)
            current_image = vision_service.take_image()
            horizontal_movement_command = (
                ohmmeter_alignment_corrector.calculate_horizontal_correction(
                    current_image
                )
            )
            if horizontal_movement_command.get_direction() == Direction.STOP:
                movement_service.execute_movement_command(horizontal_movement_command)
                break
