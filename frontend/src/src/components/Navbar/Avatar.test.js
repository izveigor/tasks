import React from 'react';
import { render, unmountComponentAtNode } from "react-dom";
import { fireEvent, screen } from '@testing-library/react';
import { act } from "react-dom/test-utils";
import Avatar from "./Avatar";

let container = null;
beforeEach(() => {
    container = document.createElement("div");
    document.body.appendChild(container);
});

afterEach(() => {
    unmountComponentAtNode(container);
    container.remove();
    container = null;
})

it("Меняем видимость меню профиля при нажатии", () => {
    const onChange = jest.fn();
    act(() => {
        render(<Avatar onChange={onChange} />, container);
    });

    const avatarButton = screen.getByRole('button');

    expect(
        container.querySelector('[data-testid="profile-menu-test"]') === null
    ).toBe(true);

    act(() => {
        fireEvent.click(avatarButton);
    });

    expect(onChange).toHaveBeenCalledTimes(1);
    expect(
        container.querySelector('[data-testid="profile-menu-test"]') !== null
    ).toBe(true);
});