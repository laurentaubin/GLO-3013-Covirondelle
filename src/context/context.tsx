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
    BOOT = "boot",
    START_GAME_CYCLE = "START_GAME_CYCLE",
    READ_RESISTANCE = "READ_RESISTANCE",
    READ_COMMAND_PANEL = "READ_COMMAND_PANEL",
    TRANSPORT_PUCK = "TRANSPORT_PUCK",
    GO_PARK = "GO_PARK",
    STOP = "STOP"
}

enum ZoneCorner {
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
    puckColors: PuckColor[]
    currentPuck: PuckColor
    currentStage: Stage
    startingZoneCornersOrder: ZoneCorner[],
    robotPose: Position,
    tableImage: unknown,
    batteryConsumption: number,
    isGameStarted: boolean
}

const initialState: ApplicationState = {
    puckColors: [],
    currentPuck: PuckColor.NONE,
    currentStage: Stage.BOOT,
    startingZoneCornersOrder: [],
    robotPose: initialPosition,
    tableImage: null,
    batteryConsumption: 0,
    isGameStarted: false
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
