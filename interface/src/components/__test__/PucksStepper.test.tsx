import React from 'react'
import ReactDOM from 'react-dom'
import PucksStepper from "../PucksStepper";

import {cleanup, render} from '@testing-library/react'
import "@testing-library/jest-dom/extend-expect"

import renderer from "react-test-renderer"
import {PuckColor, ZoneCorner} from "../../context/context";

const SOME_PUCKS = [PuckColor.BLUE, PuckColor.GREEN]
const AN_INDEX = 0
const SOME_CORNERS = [ZoneCorner.A, ZoneCorner.B]
afterEach(cleanup)

it("renders without crashing", () => {
    const div = document.createElement("div");
    ReactDOM.render(<PucksStepper pucks={SOME_PUCKS} activePuckIndex={AN_INDEX} corners={SOME_CORNERS} />, div)
})

it("renders pucks stepper correctly", () => {
    const { getByTestId } = render(<PucksStepper pucks={SOME_PUCKS} activePuckIndex={AN_INDEX} corners={SOME_CORNERS}/>)
    expect(getByTestId("pucks-stepper")).toBeTruthy()
})

// if failing and should pass, try update snapshot with "u" option
it("matches snapshot", () => {
    const tree = renderer.create(<PucksStepper pucks={SOME_PUCKS} activePuckIndex={AN_INDEX} corners={SOME_CORNERS}/>).toJSON()
    expect(tree).toMatchSnapshot()
})
