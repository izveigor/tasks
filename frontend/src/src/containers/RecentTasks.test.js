import React from 'react';

import { render, unmountComponentAtNode } from "react-dom";
import { act } from 'react-dom/test-utils';

import RecentTasks from './RecentTasks';

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
    const fakeTasksData =     [
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

    jest.spyOn(global, "fetch").mockImplementation(() =>
        Promise.resolve({
            json: () => Promise.resolve(fakeTasksData)
        })
    );

    await act(async() => {
        render(<RecentTasks />, container)
    });
    
    for (let i = 0; i > fakeTasksData.length; i++) {
        let task = container.querySelector(`[data-testid='task-${i.toString()}]`);
        expect(
            task.querySelector('[data-testid="task-title-test"]').textContent
        ).toEqual(fakeTasksData[i].title);
        expect(
            task.querySelector('[data-testid="task-time-test"]').textContent
        ).toEqual(fakeTasksData[i].time.toString());
        expect(
            task.querySelector('[data-testid="task-description-test"]').textContent
        ).toEqual(fakeTasksData[i].description);
    }
});
