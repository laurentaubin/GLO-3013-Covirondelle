import React from 'react'
import ReactDOM from 'react-dom'
import RobotStepper from "../RobotStepper";

import { render, cleanup } from '@testing-library/react'
import "@testing-library/jest-dom/extend-expect"

import renderer from "react-test-renderer"
import {Stage} from "../../context/context";

const A_STAGE = Stage.BOOT

afterEach(cleanup)

it("renders without crashing", () => {
    const div = document.createElement("div");
    ReactDOM.render(<RobotStepper activeStage={A_STAGE}/>, div)
})

it("renders pucks stepper correctly", () => {
    const { getByTestId } = render(<RobotStepper activeStage={A_STAGE}/>)
    expect(getByTestId("robot-stepper")).toBeTruthy()
})

// TODO: add check for each element to be truthy

// if failing and should pass, try update snapshot with "u" option
it("matches snapshot", () => {
    const tree = renderer.create(<RobotStepper activeStage={A_STAGE}/>).toJSON()
    expect(tree).toMatchSnapshot()
})
