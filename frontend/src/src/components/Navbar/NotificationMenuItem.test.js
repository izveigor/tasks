import React from 'react';


import { render, unmountComponentAtNode } from "react-dom";
import { act } from 'react-dom/test-utils';

import NotificationMenuItem from "./NotificationMenuItem";

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

it("Проверяем воспроизводство props у NotificationMenuItem", () => {
    act(() => {
        render(<NotificationMenuItem text="Уведомление 1" time="18.10.2022 21:13" image="https://image" />, container);
    });
    expect(
        container.querySelector("[data-testid='notification-text']").textContent
    ).toEqual("Уведомление 1");
    expect(
        container.querySelector("[data-testid='notification-time']").textContent
    ).toEqual("18.10.2022 21:13");
    expect(
        container.querySelector("[data-testid='notification-image']")
    ).toHaveAttribute('src', 'https://image');
});