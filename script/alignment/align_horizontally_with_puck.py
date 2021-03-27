import cv2
import time

import serial

from config.config import (
    EMBEDDED_CAMERA_IMAGE_SIZE,
    ROBOT_MAXIMUM_SPEED,
    SERVOING_CONSTANT,
    BASE_COMMAND_DURATION,
    STM_PORT_NAME,
    STM_BAUD_RATE,
)
from domain.Position import Position
from domain.alignment.IAlignmentCorrector import IAlignmentCorrector
from domain.movement.Direction import Direction
from domain.movement.MovementCommand import MovementCommand
from domain.movement.MovementCommandFactory import MovementCommandFactory
from domain.movement.MovementFactory import MovementFactory
from domain.vision.Color import Color
from infra.alignment.PuckAlignmentCorrector import PuckAlignmentCorrector
from infra.motor_controller.StmMotorController import StmMotorController
from infra.vision.OpenCvPuckDetector import OpenCvPuckDetector
from service.movement.MovementService import MovementService


class FakeCamera:
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


class FakeVisionService:
    def __init__(
        self,
        embedded_camera: FakeCamera,
    ):
        self._embedded_camera = embedded_camera

    def take_image(self):
        return self._embedded_camera.take_image()


class HorizontalAlignmentCorrector:
    def __init__(
        self,
        movement_service: MovementService,
        vision_service: FakeVisionService,
        puck_alignment_corrector: IAlignmentCorrector,
    ):
        self._movement_service = movement_service
        self._vision_service = vision_service
        self._puck_alignment_corrector = puck_alignment_corrector

    def correct_horizontal_alignment(self, puck_color: Color):
        current_image = self._vision_service.take_image()
        horizontal_movement_command = (
            self._puck_alignment_corrector.calculate_horizontal_correction(
                current_image, puck_color
            )
        )
        if horizontal_movement_command.get_direction() == Direction.STOP:
            return
        else:
            self._align_horizontally(horizontal_movement_command, puck_color)

    def _align_horizontally(
        self, horizontal_movement_command: MovementCommand, puck_color: Color
    ) -> None:
        self._movement_service.execute_movement_command(horizontal_movement_command)
        while True:
            time.sleep(0.5)
            current_image = self._vision_service.take_image()
            horizontal_movement_command = (
                self._puck_alignment_corrector.calculate_horizontal_correction(
                    current_image, puck_color
                )
            )
            if horizontal_movement_command.get_direction() == Direction.STOP:
                self._movement_service.execute_movement_command(
                    horizontal_movement_command
                )
                break


if __name__ == "__main__":
    image_center = Position(320, 240)
    camera = FakeCamera(0)
    vision_service = FakeVisionService(camera)
    puck_detector = OpenCvPuckDetector()
    serial = serial.Serial(port=STM_PORT_NAME, baudrate=STM_BAUD_RATE)
    stm_motor_controller = StmMotorController(serial)
    movement_service = MovementService(
        MovementFactory(),
        MovementCommandFactory(
            ROBOT_MAXIMUM_SPEED, SERVOING_CONSTANT, BASE_COMMAND_DURATION
        ),
        stm_motor_controller,
    )
    puck_alignment_corrector = PuckAlignmentCorrector(image_center, 10, puck_detector)

    horizontal_alignment_corrector = HorizontalAlignmentCorrector(
        movement_service, vision_service, puck_alignment_corrector
    )

    puck_color_to_align = Color.RED

    horizontal_alignment_corrector.correct_horizontal_alignment(puck_color_to_align)
