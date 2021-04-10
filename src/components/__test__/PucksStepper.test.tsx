import React from 'react'
import ReactDOM from 'react-dom'
import PucksStepper from "../PucksStepper";

import { render, cleanup } from '@testing-library/react'
import "@testing-library/jest-dom/extend-expect"

import renderer from "react-test-renderer"
import {PuckColor} from "../../context/context";

const SOME_PUCKS = [PuckColor.BLUE, PuckColor.GREEN]
const AN_INDEX = 0
afterEach(cleanup)

it("renders without crashing", () => {
    const div = document.createElement("div");
    ReactDOM.render(<PucksStepper pucks={SOME_PUCKS} activePuck={AN_INDEX}/>, div)
})

it("renders pucks stepper correctly", () => {
    const { getByTestId } = render(<PucksStepper pucks={SOME_PUCKS} activePuck={AN_INDEX}/>)
    expect(getByTestId("pucks-stepper")).toBeTruthy()
})

// TODO: add check for each element to be truthy

// if failing and should pass, try update snapshot with "u" option
it("matches snapshot", () => {
    const tree = renderer.create(<PucksStepper pucks={SOME_PUCKS} activePuck={AN_INDEX}/>).toJSON()
    expect(tree).toMatchSnapshot()
})
