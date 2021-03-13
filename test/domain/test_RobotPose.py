from unittest import TestCase

from domain.Orientation import Orientation
from domain.Position import Position
from domain.RobotPose import RobotPose


class TestRobotPose(TestCase):
    A_X_POSITION = 543
    ANOTHER_X_POSITION = 3
    A_Y_POSITION = 120
    ANOTHER_Y_POSITION = 800
    AN_ORIENTATION = 254
    ANOTHER_ORIENTATION = 83

    def test_givenTwoRobotPosesWithSameOrientationAndPosition_whenEqual_thenReturnTrue(
        self,
    ):
        a_robot_pose = _create_robot_pose(
            self.A_X_POSITION, self.A_Y_POSITION, self.AN_ORIENTATION
        )
        another_robot_pose = _create_robot_pose(
            self.A_X_POSITION, self.A_Y_POSITION, self.AN_ORIENTATION
        )

        are_robot_poses_equal = a_robot_pose == another_robot_pose

        self.assertTrue(are_robot_poses_equal)

    def test_givenTwoRobotPosesWithDifferentPosition_whenEqual_thenReturnFalse(self):
        a_robot_pose = _create_robot_pose(
            self.A_X_POSITION, self.A_Y_POSITION, self.AN_ORIENTATION
        )
        another_robot_pose = _create_robot_pose(
            self.ANOTHER_X_POSITION, self.ANOTHER_Y_POSITION, self.AN_ORIENTATION
        )

        are_robot_poses_equal = a_robot_pose == another_robot_pose

        self.assertFalse(are_robot_poses_equal)

    def test_givenTwoRobotPosesWithDifferentOrientation_whenEqual_thenReturnFalse(self):
        a_robot_pose = _create_robot_pose(
            self.A_X_POSITION, self.A_Y_POSITION, self.AN_ORIENTATION
        )
        another_robot_pose = _create_robot_pose(
            self.A_X_POSITION, self.A_Y_POSITION, self.ANOTHER_ORIENTATION
        )

        are_robot_poses_equal = a_robot_pose == another_robot_pose

        self.assertFalse(are_robot_poses_equal)


def _create_robot_pose(x_position: int, y_position: int, orientation: int):
    position = Position(x_position, y_position)
    orientation = Orientation(orientation)
    return RobotPose(position, orientation)
