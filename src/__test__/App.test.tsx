import React from 'react'
import ReactDOM from 'react-dom'
import App from "../App";

import { render, cleanup } from '@testing-library/react'
import "@testing-library/jest-dom/extend-expect"

import renderer from "react-test-renderer"

afterEach(cleanup)

it("renders without crashing", () => {
    const div = document.createElement("div");
    ReactDOM.render(<App/>, div)
})

it("renders app correctly", () => {
    const { getByTestId } = render(<App/>)
    expect(getByTestId("app")).toBeTruthy()
})

it("matches snapshot", () => {
    const tree = renderer.create(<App/>).toJSON()
    expect(tree).toMatchSnapshot()
})

