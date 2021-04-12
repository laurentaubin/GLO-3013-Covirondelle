import React, {createContext, useReducer} from 'react';
import {appReducer} from "./reducer";

export enum PuckColor {
    NONE = "NONE",
    BLACK = "BLACK",
    BROWN = "BROWN",
    RED = "RED",
    ORANGE = "ORANGE",
    YELLOW = "YELLOW",
    GREEN = "GREEN",
    BLUE = "BLUE",
    PURPLE = "PURPLE",
    GREY = "GREY",
    WHITE = "WHITE"
}

export enum Stage {
    boot = "boot",
    start_cycle = "start_cycle",
    go_to_ohmmeter = "go_to_ohmmeter",
    find_command_panel = "find_command_panel",
    transport_puck = "transport_puck",
    go_park = "go_park",
    stop = "stop"
}

export enum ZoneCorner {
    A = "A",
    B = "B",
    C = "C",
    D = "D"
}

interface Position {
    x: number;
    y: number;
}

const initialPosition = {
    x: 0,
    y: 0
}

export interface ApplicationState {
    Resistance: number | undefined
    PuckColors: PuckColor[]
    CurrentPuck: PuckColor | undefined
    CurrentStage: Stage | undefined
    ZoneCornersOrder: ZoneCorner[]
    RobotPosition: Position | undefined
    TableImage: string |  undefined
    BatteryElectricCharge: number | undefined,
    RobotConsumption: number,
    BatteryTime: number | undefined,
    IsGripperHolding: boolean,
    IsGameStarted: boolean
}

const initialState: ApplicationState = {
    Resistance: undefined,
    PuckColors: [],
    CurrentPuck: undefined,
    CurrentStage: undefined,
    ZoneCornersOrder: [],
    RobotPosition: undefined,
    TableImage: undefined,
    BatteryElectricCharge: undefined,
    RobotConsumption: 0,
    BatteryTime: undefined,
    IsGripperHolding: false,
    IsGameStarted: false
}

const AppContext = createContext<{
    state: ApplicationState;
    dispatch: React.Dispatch<any>;
}>({
    state: initialState,
    dispatch: () => null
});

const AppProvider: React.FC = ({children}: any) => {
    const [state, dispatch] = useReducer(appReducer, initialState);

    return (
        <AppContext.Provider value={{state, dispatch}}>
            {children}
        </AppContext.Provider>
    )
}

export {AppContext, AppProvider};
