import React from 'react';

import { render, unmountComponentAtNode } from "react-dom";
import { act } from 'react-dom/test-utils';

import Task from './Task';

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

it('Проверяем props', () => {
    const propsData = 
    [
        {
            'name': 'Сделать отчет о страусах',
            'time': '20 минут',
            'image': 'https://image',
            'status': 'Успешно',
        }, 
        {
            'name': 'Сделать отчет о воробьях',
            'time': '30 минут',
            'image': 'https://image2',
            'status': 'Обработка',
        }, 
        {
            'name': 'Сделать отчет о сороках',
            'time': '40 минут',
            'image': 'https://image3',
            'status': 'Закрыто',
        },
    ];

    propsData.forEach(data => {
        act(() => {
            render(<Task name={data.name}
                        time={data.time}
                        image={data.image}
                        status={data.status}
                    />, container);
        });

        expect(
            container.querySelector("[data-testid='task-name-test']").textContent
        ).toEqual(data.name);
        expect(
            container.querySelector("[data-testid='task-time-test']").textContent
        ).toEqual(data.time);
        expect(
            container.querySelector("[data-testid='task-image-test']")
        ).toHaveAttribute('src', data.image);
        expect(
            container.querySelector("[data-testid='task-status-test']").textContent
        ).toEqual(data.status);
    });
});
