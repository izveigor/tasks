import React from 'react';

import { render, unmountComponentAtNode } from "react-dom";
import { act } from 'react-dom/test-utils';

import CurrentTask from './CurrentTask';

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

it('Проверяем props', async() => {
    const fakeTaskData = {
        "description": "Новое задание!",
        "title": "Задание 1",
        "time": Date.now(),
    }

    jest.spyOn(global, "fetch").mockImplementation(() =>
        Promise.resolve({
            json: () => Promise.resolve(fakeTaskData)
        })
    );

    await act(async() => {
        render(<CurrentTask />, container);
    });
    
    expect(
        container.querySelector('[data-testid="task-title-test"]').textContent
    ).toEqual(fakeTaskData.title);
    expect(
        container.querySelector('[data-testid="task-time-test"]').textContent
    ).toEqual(fakeTaskData.time.toString());
    expect(
        container.querySelector('[data-testid="task-description-test"]').textContent
    ).toEqual(fakeTaskData.description);
});
