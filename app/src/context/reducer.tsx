export enum ActionType {
    UPDATE_STATE = "UPDATE_STATE"
}

export const appReducer = (state: any, action: any) => {
    switch (action.type) {
        case ActionType.UPDATE_STATE:
            console.log(action)
            return {
                ...state,
                puckColors: action.payload._puck_colors,
                currentPuck: action.payload._current_puck,
                currentStage: action.payload._current_stage,
                startingZoneCornersOrder: action.payload._starting_zone_corner_order,
                robotPose: action.payload._robot_position,
                tableImage: action.payload._encoded_table_image,
                batteryConsumption: action.payload._battery_consumption
            }
        default:
            return state;
    }
}