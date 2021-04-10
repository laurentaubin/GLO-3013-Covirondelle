import React from 'react'
import ReactDOM from 'react-dom'
import DataCard from "../DataCard";

import { render, cleanup } from '@testing-library/react'
import "@testing-library/jest-dom/extend-expect"

import renderer from "react-test-renderer"

const A_STRING = "a title"
const A_VALUE = 5

afterEach(cleanup)

it("renders without crashing", () => {
    const div = document.createElement("div");
    ReactDOM.render(<DataCard title={A_STRING} value={A_VALUE} unit={A_STRING}/>, div)
})

it("renders title of data card correctly", () => {
    const aTitle = "my title"
    const { getByTestId } = render(<DataCard title={aTitle} value={A_VALUE} unit={A_STRING}/>)
    expect(getByTestId("data-card")).toHaveTextContent(aTitle)
})

it("renders value of data card correctly", () => {
    const someValue = 3
    const { getByTestId } = render(<DataCard title={A_STRING} value={someValue} unit={A_STRING}/>)
    expect(getByTestId("data-card")).toHaveTextContent(someValue.toString())
})

it("renders unit of data card correctly", () => {
    const aUnit = "blabla unit"
    const { getByTestId } = render(<DataCard title={A_STRING} value={A_VALUE} unit={aUnit}/>)
    expect(getByTestId("data-card")).toHaveTextContent(aUnit)
})

// if failing and should pass, try update snapshot with "u" option
it("matches snapshot", () => {
    const tree = renderer.create(<DataCard title={A_STRING} value={A_VALUE} unit={A_STRING}/>).toJSON()
    expect(tree).toMatchSnapshot()
})
