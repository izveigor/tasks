import React from 'react';
import { screen, fireEvent, render } from '@testing-library/react';
import { act } from 'react-dom/test-utils';
import {
    BrowserRouter as Router
} from 'react-router-dom';
import store from '../features/store';
import { Provider } from 'react-redux';
import ChangeUsername  from './ChangeUsername';


it('Проверяем сообщение, если имя пользователя уже используется', async() => {
    const response = {
        "exist": true,
        "available": "username1",
    };
    const username = "username";
    jest.spyOn(global, "fetch").mockImplementation(() =>
        Promise.resolve({
            json: () => Promise.resolve(response)
        })
    );

    await act(async() => {
        render(<Provider store={store}><Router><ChangeUsername /></Router></Provider>);
    });

    const usernameInput = document.querySelector('[data-testid="username-input"]');
    await act(async() => {
        fireEvent.change(usernameInput, { target: { value: username}});
    });

    expect(usernameInput.value).toBe(username);
    expect(
        document.querySelector('[data-testid="username-exist"]').textContent
    ).toEqual('Такой пользователь уже существует! Доступное имя: "' + response['available'] + '".');

    global.fetch.mockRestore();
});


it('Меняем имя пользователя', async() => {
    const response = {
        "exist": false,
        "available": "",
    };
    const username = "username";
    await act(async() => {
        render(<Provider store={store}><Router><ChangeUsername /></Router></Provider>);
    });

    jest.spyOn(global, "fetch").mockImplementation(() =>
        Promise.resolve({
            ok: true,
            json: () => Promise.resolve(response)
        })
    );

    const usernameInput = document.querySelector('[data-testid="username-input"]');
    await act(async() => {
        fireEvent.change(usernameInput, { target: { value: username }});
    });

    expect(usernameInput.value).toBe(username);

    const changeButton = screen.getByRole('button');
    await act(async() => {
        fireEvent.click(changeButton);
    });

    expect(
        document.querySelector('[data-testid="changed-successfully"]').textContent
    ).toEqual('Имя пользователя было успешно изменено!');
    global.fetch.mockRestore();
});