import serial

from config.config import (
    STM_PORT_NAME,
    STM_BAUD_RATE,
    BASE_COMMAND_DURATION,
    SERVOING_CONSTANT,
    ROBOT_MAXIMUM_SPEED,
)
from domain.movement.MovementCommandFactory import MovementCommandFactory
from domain.movement.MovementFactory import MovementFactory
from domain.movement.Path import Path
from domain.movement.Position import Position
from infra.communication.motor_controller.StmMotorController import StmMotorController
from service.movement.MovementService import MovementService

if __name__ == "__main__":
    straight_path = Path([])

    for i in range(1000):
        position = Position(100 + i, 100)
        straight_path.add(position)

    turn_path = Path([])

    for i in range(500):
        position = Position(100 + i, 100)
        turn_path.add(position)
    print(turn_path[-1].get_x_coordinate())

    for i in range(500):
        position = Position(599, 101 + i)
        turn_path.add(position)

    movement_command_factory = MovementCommandFactory(
        ROBOT_MAXIMUM_SPEED, SERVOING_CONSTANT, BASE_COMMAND_DURATION
    )
    motor_controller = StmMotorController(
        serial.Serial(STM_PORT_NAME, STM_BAUD_RATE), movement_command_factory
    )

    movement_factory = MovementFactory()
    movement_service = MovementService(movement_factory, motor_controller)

    print("----------- Straight path -------------")
    input("Press any key when ready to start......")
    movement_service.move(straight_path)

    print(" -------- Straight path over ----------")

    input("Press any key when ready to continue......")
    print()

    print("----------- Turning Path --------------")
    input("Press any key when ready to start......")
    movement_service.move(turn_path)
