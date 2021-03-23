from config.config import (
    SERVO_SPEED,
    SERVO_ACCELERATION,
    MAX_HORIZONTAL_ANGLE_VALUE,
    MIN_HORIZONTAL_ANGLE_VALUE,
    MAX_VERTICAL_ANGLE_VALUE,
    MIN_VERTICAL_ANGLE_VALUE,
    CAMERA_HORIZONTAL_SERVO_ID,
    CAMERA_VERTICAL_SERVO_ID,
)


class CameraControl:
    def __init__(self, maestro):
        self.maestro = maestro

        self.horizontalAngle = 90
        self.verticalAngle = 90
        self.maestro.setSpeed(CAMERA_HORIZONTAL_SERVO_ID, SERVO_SPEED)
        self.maestro.setSpeed(CAMERA_VERTICAL_SERVO_ID, SERVO_SPEED)
        self.maestro.setAccel(CAMERA_HORIZONTAL_SERVO_ID, SERVO_ACCELERATION)
        self.maestro.setAccel(CAMERA_VERTICAL_SERVO_ID, SERVO_ACCELERATION)

        self.set_horizontal_angle(self.horizontalAngle)

    def set_horizontal_angle(self, angle):
        self.horizontalAngle = angle
        conversion = (
            angle / 360 * (MAX_HORIZONTAL_ANGLE_VALUE - MIN_HORIZONTAL_ANGLE_VALUE)
            + MIN_HORIZONTAL_ANGLE_VALUE
        )
        self.maestro.setTarget(CAMERA_HORIZONTAL_SERVO_ID, conversion)

    def set_vertical_angle(self, angle):
        self.verticalAngle = angle
        conversion = (
            angle / 360 * (MAX_VERTICAL_ANGLE_VALUE - MIN_VERTICAL_ANGLE_VALUE)
            + MIN_VERTICAL_ANGLE_VALUE
        )
        self.maestro.setTarget(CAMERA_VERTICAL_SERVO_ID, conversion)

    def get_horizontal_angle(self):
        return self.horizontalAngle

    def get_vertical_angle(self):
        return self.verticalAngle
