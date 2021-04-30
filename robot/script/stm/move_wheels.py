import serial

from config.config import (
    STM_PORT_NAME,
    STM_BAUD_RATE,
    BASE_COMMAND_DURATION,
    SERVOING_CONSTANT,
    ROBOT_MAXIMUM_SPEED,
)
from domain.movement.CommandDuration import CommandDuration
from domain.movement.Direction import Direction
from domain.movement.Distance import Distance
from domain.movement.Movement import Movement
from domain.movement.MovementCommandFactory import MovementCommandFactory
from domain.movement.Speed import Speed
from infra.motor_controller.StmMotorController import StmMotorController
from service.movement.MovementService import MovementService

if __name__ == "__main__":
    straight_movements = [Movement(Direction.FORWARD, Distance(1))]
    turn_movements = [
        Movement(Direction.FORWARD, Distance(0.5)),
        Movement(Direction.LEFT, Distance(0.5)),
    ]

    movement_command_factory = MovementCommandFactory(
        Speed(ROBOT_MAXIMUM_SPEED),
        Speed(SERVOING_CONSTANT),
        CommandDuration(BASE_COMMAND_DURATION),
    )
    motor_controller = StmMotorController(serial.Serial(STM_PORT_NAME, STM_BAUD_RATE))

    movement_service = MovementService(movement_command_factory, motor_controller)

    print("----------- Straight path -------------")
    input("Press any key when ready to start......")
    movement_service.move(straight_movements)

    print(" -------- Straight path over ----------")

    input("Press any key when ready to continue......")
    print()

    print("----------- Turning Path --------------")
    input("Press any key when ready to start......")
    movement_service.move(turn_movements)
