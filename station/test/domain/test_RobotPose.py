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
    FIRST_QUADRANT_ORIENTATION = 45
    SECOND_QUADRANT_ORIENTATION = 120
    THIRD_QUADRANT_ORIENTATION = 190
    FOURTH_QUADRANT_ORIENTATION = 315

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

    def test_givenRobotPoseWithFirstQuadrantOrientation_whenGetGripperPosition_thenReturnCorrectPosition(
        self,
    ):
        a_robot_pose = _create_robot_pose(
            self.A_X_POSITION, self.A_Y_POSITION, self.FIRST_QUADRANT_ORIENTATION
        )

        actual_gripper_position = a_robot_pose.get_gripper_position()

        x_position_is_greater = (
            actual_gripper_position.get_x_coordinate() > self.A_X_POSITION
        )
        y_position_is_smaller = (
            actual_gripper_position.get_y_coordinate() < self.A_Y_POSITION
        )

        self.assertTrue(x_position_is_greater)
        self.assertTrue(y_position_is_smaller)

    def test_givenRobotPoseWithSecondQuadrantOrientation_whenGetGripperPosition_thenReturnCorrectPosition(
        self,
    ):
        a_robot_pose = _create_robot_pose(
            self.A_X_POSITION, self.A_Y_POSITION, self.SECOND_QUADRANT_ORIENTATION
        )

        actual_gripper_position = a_robot_pose.get_gripper_position()

        x_position_is_smaller = (
            actual_gripper_position.get_x_coordinate() < self.A_X_POSITION
        )
        y_position_is_smaller = (
            actual_gripper_position.get_y_coordinate() < self.A_Y_POSITION
        )

        self.assertTrue(x_position_is_smaller)
        self.assertTrue(y_position_is_smaller)

    def test_givenRobotPoseWithThirdQuadrantOrientation_whenGetGripperPosition_thenReturnCorrectPosition(
        self,
    ):
        a_robot_pose = _create_robot_pose(
            self.A_X_POSITION, self.A_Y_POSITION, self.THIRD_QUADRANT_ORIENTATION
        )

        actual_gripper_position = a_robot_pose.get_gripper_position()

        x_position_is_smaller = (
            actual_gripper_position.get_x_coordinate() < self.A_X_POSITION
        )
        y_position_is_greater = (
            actual_gripper_position.get_y_coordinate() > self.A_Y_POSITION
        )

        self.assertTrue(x_position_is_smaller)
        self.assertTrue(y_position_is_greater)

    def test_givenRobotPoseWithFourthQuadrantOrientation_whenGetGripperPosition_thenReturnCorrectPosition(
        self,
    ):
        a_robot_pose = _create_robot_pose(
            self.A_X_POSITION, self.A_Y_POSITION, self.FOURTH_QUADRANT_ORIENTATION
        )

        actual_gripper_position = a_robot_pose.get_gripper_position()

        x_position_is_greater = (
            actual_gripper_position.get_x_coordinate() > self.A_X_POSITION
        )
        y_position_is_greater = (
            actual_gripper_position.get_y_coordinate() > self.A_Y_POSITION
        )

        self.assertTrue(x_position_is_greater)
        self.assertTrue(y_position_is_greater)


def _create_robot_pose(x_position: int, y_position: int, orientation: int):
    position = Position(x_position, y_position)
    orientation = Orientation(orientation)
    return RobotPose(position, orientation)
