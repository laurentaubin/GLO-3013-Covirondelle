import React from 'react'
import ReactDOM from 'react-dom'
import StateCard from "../StateCard";

import {cleanup, render} from '@testing-library/react'
import "@testing-library/jest-dom/extend-expect"

import renderer from "react-test-renderer"

const A_STRING = "blabla string"

afterEach(cleanup)

it("renders without crashing", () => {
    const div = document.createElement("div");
    ReactDOM.render(<StateCard title={A_STRING} active={A_STRING} neutral={A_STRING} isActive={true}/>, div)
})

it("renders title of state card correctly", () => {
    const aTitle = "patate"
    const {getByTestId} = render(<StateCard title={aTitle} active={A_STRING} neutral={A_STRING} isActive={true}/>)
    expect(getByTestId("state-card")).toHaveTextContent(aTitle)
})

it("renders active label of state card correctly", () => {
    const anActiveLabel = "some label"
    const {getByTestId} = render(<StateCard title={A_STRING} active={anActiveLabel} neutral={A_STRING}
                                            isActive={true}/>)
    expect(getByTestId("state-card")).toHaveTextContent(anActiveLabel)
})

it("renders neutral label of state card correctly", () => {
    const aNeutralLabel = "label blabla"
    const {getByTestId} = render(<StateCard title={A_STRING} active={A_STRING} neutral={aNeutralLabel}
                                            isActive={true}/>)
    expect(getByTestId("state-card")).toHaveTextContent(aNeutralLabel)
})

// if failing and should pass, try update snapshot with "u" option
it("matches snapshot", () => {
    const tree = renderer.create(<StateCard title={"title"} active={"active"} neutral={"neutral"}
                                            isActive={false}/>).toJSON()
    expect(tree).toMatchSnapshot()
})
