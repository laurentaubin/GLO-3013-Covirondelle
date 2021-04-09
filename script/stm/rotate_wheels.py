import serial

from config.config import (
    STM_PORT_NAME,
    STM_BAUD_RATE,
    BASE_COMMAND_DURATION,
    SERVOING_CONSTANT,
    ROBOT_MAXIMUM_SPEED,
)
from domain.movement.CommandDuration import CommandDuration
from domain.movement.MovementCommandFactory import MovementCommandFactory
from domain.movement.Speed import Speed
from infra.motor_controller.StmMotorController import StmMotorController
from service.movement.MovementService import MovementService

if __name__ == "__main__":
    movement_command_factory = MovementCommandFactory(
        Speed(ROBOT_MAXIMUM_SPEED),
        Speed(SERVOING_CONSTANT),
        CommandDuration(BASE_COMMAND_DURATION),
    )

    motor_controller = StmMotorController(serial.Serial(STM_PORT_NAME, STM_BAUD_RATE))

    movement_service = MovementService(movement_command_factory, motor_controller)

    print("----------- Rotate 90 degrees -------------")
    input("Press any key when ready to start......")
    movement_service.rotate(90)

    print(" -------- Rotate 90 degrees over ----------")

    input("Press any key when ready to continue......")
    print()

    print("----------- Rotate negative 90 degrees --------------")
    input("Press any key when ready to start......")
    movement_service.rotate(-90)

    print(" -------- Rotate negative 90 degrees over ----------")

    input("Press any key when ready to continue......")
    print()

    print("----------- Rotate 30 degrees --------------")
    input("Press any key when ready to start......")
    movement_service.rotate(30)

    print(" -------- Rotate 30 degrees over ----------")
