import { ApplicationState } from "./context";

export enum ActionType {
  UPDATE_STATE = "UPDATE_STATE",
  START_GAME = "START_GAME",
}

export const appReducer = (state: ApplicationState, action: any) => {
  switch (action.type) {
    case ActionType.START_GAME:
      console.log(action);
      return {
        ...state,
        IsGameStarted: true,
      };
    case ActionType.UPDATE_STATE:
      console.log(action);
      return {
        ...state,
        PuckColors: action.payload._puck_colors,
        CurrentPuck: action.payload._current_puck,
        CurrentStage: action.payload._current_stage,
        ZoneCornersOrder: action.payload._starting_zone_corner_order,
        RobotPosition: action.payload._robot_position,
        RobotConsumption: action.payload._battery_consumption,
        currentPlannedTrajectory: action.payload._current_planned_trajectory,
        BatteryTime: action.payload._battery_time_left,
        BatteryElectricCharge: action.payload._battery_percentage,
        IsGripperHolding: action.payload._gripper_state === 1,
        Resistance: action.payload._resistance_value,
        IsRobotBooted: action.payload._is_robot_booted,
        IsGameStarted: action.payload._is_game_started,
      };
    default:
      return state;
  }
};
