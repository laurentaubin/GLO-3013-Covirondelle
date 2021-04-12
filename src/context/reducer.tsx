import {ApplicationState} from "./context";

export enum ActionType {
    UPDATE_STATE = "UPDATE_STATE",
    START_GAME = "START_GAME"
}

export const appReducer = (state: ApplicationState, action: any) => {
    switch (action.type) {
        case ActionType.START_GAME:
            console.log(action)
            return {
                ...state,
                isGameStarted: true
            }
        case ActionType.UPDATE_STATE:
            console.log(action)
            // TODO: check payload if all information is received
            return {
                ...state,
                PuckColors: action.payload._puck_colors,
                CurrentPuck: action.payload._current_puck,
                CurrentStage: action.payload._current_stage,
                ZoneCornersOrder: action.payload._starting_zone_corner_order,
                RobotPosition: action.payload._robot_position,
                TableImage: action.payload._encoded_table_image,
                RobotConsumption: action.payload._battery_consumption
            }
        default:
            return state;
    }
}
