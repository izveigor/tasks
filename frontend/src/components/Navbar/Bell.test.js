import React from 'react';
import { render, unmountComponentAtNode } from "react-dom";
import { fireEvent, screen } from '@testing-library/react';
import { act } from "react-dom/test-utils";
import Bell from "./Bell";

let container = null;
beforeEach(() => {
    container = document.createElement("div");
    document.body.appendChild(container);
});

afterEach(() => {
    unmountComponentAtNode(container);
    container.remove();
    container = null;
});

it("Меняем видимость уведомлений при нажатии", async() => {
    const onChange = jest.fn();
    const fakeNotifications = {
        "content": [],
    };

    jest.spyOn(global, "fetch").mockImplementation(() =>
        Promise.resolve({
            json: () => Promise.resolve(fakeNotifications)
        })
    );

    await act(async() => {
        render(<Bell onChange={onChange} />, container);
    });

    const bellButton = screen.getByRole('button');

    expect(
        container.querySelector('[data-testid="notification-menu-test"]') === null
    ).toBe(true);

    await act(async() => {
        fireEvent.click(bellButton);
    });

    expect(onChange).toHaveBeenCalledTimes(1);
    expect(
        container.querySelector('[data-testid="notification-menu-test"]') !== null
    ).toBe(true);

    global.fetch.mockRestore();
});