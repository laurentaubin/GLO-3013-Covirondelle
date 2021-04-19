import React, {useContext, useEffect, useRef, useState} from "react";
import tableImage from "./images/tableImage.jpg"
import {AppContext} from "../context/context";

const TableDisplay = () => {
    const PLANNED_TRAJECTORY_COLOR = '#0000FF'
    const ROBOT_REAL_PATH_COLOR = '#ff0000'
    const IMAGE_RATIO = 2.5
    const {state} = useContext(AppContext);
    const [image, setImage] = useState(null)
    const canvas = useRef(null)
    const [lastRobotPosition, setLastRobotPosition] = useState({x_coordinate: 0, y_coordinate: 0})

    useEffect(() => {
        const baseTableImage = new Image();
        baseTableImage.src = tableImage
        // @ts-ignore
        baseTableImage.onload = () => setImage(baseTableImage)
    }, [])

    useEffect(() => {
        if (image && canvas) {
            // @ts-ignore
            const context = canvas.current.getContext("2d");
            context.drawImage(image, 0, 0, 640, 480);
        }
    }, [image, canvas])

    useEffect(() => {
        // @ts-ignore
        const context = canvas.current.getContext("2d");
        if (context !== null) {
            const x_current_position = state.RobotPosition?.x_coordinate ?? 0 / IMAGE_RATIO
            const y_current_position = state.RobotPosition?.y_coordinate ?? 0 / IMAGE_RATIO
            context.beginPath()
            if (lastRobotPosition.x_coordinate == 0 && lastRobotPosition.y_coordinate == 0) {
                context.moveTo(x_current_position, y_current_position)
            } else {
                context.moveTo(lastRobotPosition.x_coordinate, lastRobotPosition.y_coordinate)
            }
            context.lineTo(x_current_position, y_current_position)
            context.strokeStyle = ROBOT_REAL_PATH_COLOR;
            context.stroke();
            setLastRobotPosition({
                x_coordinate: x_current_position,
                y_coordinate: y_current_position
            })
        }
    }, [state.RobotPosition])

    useEffect(() => {
        if (state.currentPlannedTrajectory.length !== 0) {
            // @ts-ignore
            const context = canvas.current.getContext("2d");
            if (context !== null) {
                context.beginPath()
                let lastPosition = state.currentPlannedTrajectory[0]
                context.strokeStyle = PLANNED_TRAJECTORY_COLOR;
                state.currentPlannedTrajectory.map(position => {
                    context.moveTo(lastPosition.x_coordinate / IMAGE_RATIO, lastPosition.y_coordinate / IMAGE_RATIO)
                    context.lineTo(position.x_coordinate / IMAGE_RATIO, position.y_coordinate / IMAGE_RATIO)
                    context.stroke()
                    lastPosition = position
                })
            }
        }
    }, [state.currentPlannedTrajectory])

    return (
        <div>
            <canvas ref={canvas} width={640} height={480}/>
        </div>
    )
}

export default TableDisplay
