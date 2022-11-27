import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { act } from 'react-dom/test-utils';
import CurrentTask from './CurrentTask';
import {
    BrowserRouter as Router
} from 'react-router-dom';
import store from '../features/store';
import { Provider } from 'react-redux';
import { userUpdated } from '../features/userSlice';


const response = {
    "title": "Название",
    "id": 1,
    "description": "Описание",
    "time": "2018-9-18T10:46:43.553472514Z"
};

it('Получаем текущее задание и пробуем его закрыть успешно', async() => {
    const response = {
        "title": "Название",
        "id": 1,
        "description": "Описание",
        "time": "2018-9-18T10:46:43.553472514Z"
    };

    jest.spyOn(global, "fetch").mockImplementation(() =>
        Promise.resolve({
            ok: true,
            json: () => Promise.resolve(response),
        })
    );

    store.dispatch(userUpdated({"isTeammate": true}));
    await act(async() => {
        render(<Provider store={store}><Router><CurrentTask /></Router></Provider>)
    });

    const currentTask = document.querySelector('[data-testid="current-task"]');
    expect(currentTask.textContent).toEqual("Текущее задание:");

    const closeSuccesfullyButton = document.querySelector('[data-testid="close-successfully"]');

    await act(async() => {
        fireEvent.click(closeSuccesfullyButton);
    });

    const emptyCurrentTask = document.querySelector('[data-testid="empty-current-task"]')
    expect(emptyCurrentTask.textContent).toEqual("Текущее задание отсутвует!");

    await act(async() => {
        store.dispatch(userUpdated({"isTeammate": false}));
    });
    global.fetch.mockRestore();
});