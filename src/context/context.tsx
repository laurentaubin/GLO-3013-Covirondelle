import React, {createContext, useReducer} from 'react';
import {appReducer} from "./reducer";

enum PuckColor {
    NONE="NONE",
    BLACK="BLACK",
    BROWN="BROWN",
    RED="RED",
    ORANGE="ORANGE",
    YELLOW=ORANGE,
    GREEN="GREEN",
    BLUE="BLUE",
    PURPLE="PURPLE",
    GREY="GREY",
    WHITE="WHITE"
}

enum Stage {
    BOOT="BOOT",
    START_GAME_CYCLE="START_GAME_CYCLE",
    READ_RESISTANCE="READ_RESISTANCE",
    READ_COMMAND_PANEL="READ_COMMAND_PANEL",
    TRANSPORT_PUCK="TRANSPORT_PUCK",
    GO_PARK="GO_PARK",
    STOP="STOP"
}

enum StartingZoneCorners {
    A="A",
    B="B",
    C="C",
    D="D"
}

interface Position {
    x: number;
    y: number;
}

interface Orientation {
    angle: number;
}

interface RobotPose {
    position: Position;
    orientation: Orientation
}

interface InitialState {
    puckColors: PuckColor[];
    currentPuck: PuckColor;
    currentStage: Stage;
    startingZoneCornersOrder: StartingZoneCorners[];
    robotPose: RobotPose;
    tableImage: unknown;
    batteryConsumption: number,
    isGameStarted: boolean
}

const initialPosition = {
    x: 0,
    y: 0
}

const initialOrientation = {
    angle: 0
}

const initialRobotPose = {
    position: initialPosition,
    orientation: initialOrientation
}

const initialState = {
    puckColors: [],
    currentPuck: PuckColor.NONE,
    currentStage: Stage.BOOT,
    startingZoneCornersOrder: [],
    robotPose: initialRobotPose,
    tableImage: null,
    batteryConsumption: 0,
    isGameStarted: false
}

const AppContext = createContext<{
    state: InitialState;
    dispatch: React.Dispatch<any>;
}>({
    state: initialState,
    dispatch: () => null
});

// eslint-disable-next-line react/prop-types
const AppProvider: React.FC = ({ children }) => {
    const [state, dispatch] = useReducer(appReducer, initialState);

    return (
        <AppContext.Provider value={{state, dispatch}}>
            {children}
        </AppContext.Provider>
    )
}

export { AppContext, AppProvider };