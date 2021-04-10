import React from 'react'
import ReactDOM from 'react-dom'
import Dashboard from "../Dashboard";

import { render, cleanup } from '@testing-library/react'
import "@testing-library/jest-dom/extend-expect"

import renderer from "react-test-renderer"

afterEach(cleanup)

it("renders without crashing", () => {
    const div = document.createElement("div");
    ReactDOM.render(<Dashboard/>, div)
})

it("renders dashboard correctly", () => {
    const { getByTestId } = render(<Dashboard/>)
    expect(getByTestId("dashboard")).toBeTruthy()
})

it("renders a title for battery charge", () => {
    const { getByText } = render(<Dashboard/>)
    expect(getByText("Charge électrique de la batterie")).toBeTruthy()
})

it("renders a title for robot power consumption", () => {
    const { getByText } = render(<Dashboard/>)
    expect(getByText("Consommation électrique du robot")).toBeTruthy()
})

it("renders a title for battery time", () => {
    const { getByText } = render(<Dashboard/>)
    expect(getByText("Temps restant à la batterie")).toBeTruthy()
})

it("renders a puck stepper", () => {
    const { getByTestId } = render(<Dashboard/>)
    expect(getByTestId("pucks-stepper")).toBeTruthy()
})

it("renders a title for gripper state", () => {
    const { getByText } = render(<Dashboard/>)
    expect(getByText("État du préhenseur")).toBeTruthy()
})

it("renders a title for robot state", () => {
    const { getByText } = render(<Dashboard/>)
    expect(getByText("État du robot")).toBeTruthy()
})

it("renders a robot stepper", () => {
    const { getByTestId } = render(<Dashboard/>)
    expect(getByTestId("robot-stepper")).toBeTruthy()
})

// if failing and should pass, try update snapshot with "u" option
it("matches snapshot", () => {
    const tree = renderer.create(<Dashboard/>).toJSON()
    expect(tree).toMatchSnapshot()
})
