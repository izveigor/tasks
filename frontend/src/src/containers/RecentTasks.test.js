import React from 'react';
import { render } from '@testing-library/react';
import { act } from 'react-dom/test-utils';
import RecentTasks from './RecentTasks';
import {
    BrowserRouter as Router
} from 'react-router-dom';
import store from '../features/store';
import { Provider } from 'react-redux';
import { USERS_URL_WITHOUT_SLASH } from '../features/constants';


it('Проверяем, если задания отсутствуют', async() => {
    jest.spyOn(global, "fetch").mockImplementation(() =>
        Promise.resolve({
            ok: false,
        })
    );

    await act(async() => {
        render(<Provider store={store}><Router><RecentTasks /></Router></Provider>)
    });

    const emptyTask = document.querySelector('[data-testid="empty-tasks"]')
    expect(emptyTask.textContent).toEqual("Задания отсутствуют!");

    global.fetch.mockRestore();
});


it('Проверяем, если задания присутствуют', async() => {
    const data = [
        {
            "receiver_user": {
                "image": "image",
            },
            "title": "Название",
            "id": 1,
            "description": "Описание",
            "time": "2018-9-18T10:46:43.553472514Z",
            "status": "Успешно",
        },
    ];

    jest.spyOn(global, "fetch").mockImplementation(() =>
        Promise.resolve({
            ok: true,
            json: () => Promise.resolve(data),
        })
    );

    await act(async() => {
        render(<Provider store={store}><Router><RecentTasks /></Router></Provider>)
    });

    expect(
        document.querySelector("[data-testid='tasks']") !== null
    ).toBe(true);
    expect(
        document.querySelector("[data-testid='task-name']").textContent
    ).toEqual(data[0].title + " #" + data[0].id.toString());
    expect(
        document.querySelector("[data-testid='task-time']").textContent
    ).toEqual(data[0].time.replace('T', ' ').split('.')[0]);
    expect(
        document.querySelector("[data-testid='task-image']")
    ).toHaveAttribute('src', USERS_URL_WITHOUT_SLASH + data[0].receiver_user.image);
    expect(
        document.querySelector("[data-testid='task-status']").textContent
    ).toEqual(data[0].status);
});