import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { act } from 'react-dom/test-utils';
import LoginFrom from './LoginForm';
import {
    BrowserRouter as Router
} from 'react-router-dom';
import store from '../../features/store';
import { Provider } from 'react-redux';
import { userUpdated } from '../../features/userSlice';

const mockUseNavigate = jest.fn();

jest.mock('react-router-dom', () => ({
    ...jest.requireActual('react-router-dom'),
    useNavigate: () => mockUseNavigate,
}));


it("Удачный вход пользователя", async() => {
    const response = {"token": "1"};
    jest.spyOn(global, "fetch").mockImplementation(() =>
        Promise.resolve({
            ok: true,
            json: () => Promise.resolve(response),
        })
    );

    await act(async() => {
        render(<Provider store={store}><Router><LoginFrom /></Router></Provider>);
    });

    const inputData = {
        "username": "username",
        "password": "password",
    };

    const usernameInput = document.querySelector('[data-testid="username-input"]');
    const passwordInput = document.querySelector('[data-testid="password-input"]');

    const loginButton = screen.getByRole('button');

    await act(async() => {
        fireEvent.change(usernameInput, { target: { value: inputData["username"] }});
        fireEvent.change(passwordInput, { target: { value: inputData["password"] }});

        fireEvent.click(loginButton);
    });

    const token = store.getState()["user"]["token"];

    expect(token).toEqual(response["token"])
    expect(mockUseNavigate).toHaveBeenCalledTimes(1);
    expect(mockUseNavigate).toHaveBeenCalledWith('/main');

    await act(async() => {
        store.dispatch(userUpdated({"token": null}));
    })
    global.fetch.mockRestore();
});


it("Неудачный вход пользователя", async() => {
    jest.spyOn(global, "fetch").mockImplementation(() =>
        Promise.resolve({
            ok: false,
            json: () => Promise.resolve({}),
        })
    );

    await act(async() => {
        render(<Provider store={store}><Router><LoginFrom /></Router></Provider>);
    });

    const inputData = {
        "username": "username",
        "password": "password",
    };

    const usernameInput = document.querySelector('[data-testid="username-input"]');
    const passwordInput = document.querySelector('[data-testid="password-input"]');

    const loginButton = screen.getByRole('button');

    await act(async() => {
        fireEvent.change(usernameInput, { target: { value: inputData["username"] }});
        fireEvent.change(passwordInput, { target: { value: inputData["password"] }});

        fireEvent.click(loginButton);
    });

    const loginError = document.querySelector('[data-testid="login-error"]');
    expect(store.getState()["user"]["token"] === null).toBe(true);
    expect(loginError.textContent).toEqual("Неверное имя пользователя или пароль!");

    global.fetch.mockRestore();
});