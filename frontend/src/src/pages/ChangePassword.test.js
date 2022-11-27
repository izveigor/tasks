import React from 'react';
import { screen, fireEvent, render } from '@testing-library/react';
import { act } from 'react-dom/test-utils';
import ChangePassword from './ChangePassword';
import {
    BrowserRouter as Router
} from 'react-router-dom';
import store from '../features/store';
import { Provider } from 'react-redux';


it('Проверяем, если пароль не соответствует стандарту', () => {
    const password = "password";
    act(() => {
        render(<Provider store={store}><Router><ChangePassword /></Router></Provider>);
    });

    const passwordInput = screen.getByPlaceholderText('Пароль');

    act(() => {
        fireEvent.change(passwordInput, { target: { value: "password"}});
    });

    expect(passwordInput.value).toBe(password);
    expect(
        document.querySelector('[data-testid="wrong-password"]').textContent
    ).toEqual("Пароль должен содержать цифры, строчные и прописные буквы! Длина пароля должна составлять не менее 10 символов!");
});


it('Проверяем, если пароль и повторный пароль не совпадают', () => {
    const password="Password11", repeatedPassword="Password1";
    act(() => {
        render(<Provider store={store}><Router><ChangePassword /></Router></Provider>);
    });

    const passwordInput = screen.getByPlaceholderText('Пароль'),
          repeatedPasswordInput = screen.getByPlaceholderText('Повторить пароль');

    act(() => {
        fireEvent.change(passwordInput, { target: { value: password }});
        fireEvent.change(repeatedPasswordInput, { target: { value: repeatedPassword}});
    });

    expect(passwordInput.value).toBe(password);
    expect(repeatedPasswordInput.value).toBe(repeatedPassword);
    expect(
        document.querySelector('[data-testid="password-not-equals-repeated-password"]').textContent
    ).toEqual("Пароли не совпадают!");
});


it('Проверяем, что пароль был успешно изменен', async() => {
    const password="Password11", repeatedPassword="Password11";
    jest.spyOn(global, "fetch").mockImplementation(() =>
        Promise.resolve({
            ok: true,
        })
    );

    await act(async() => {
        render(<Provider store={store}><Router><ChangePassword /></Router></Provider>);
    });

    const passwordInput = screen.getByPlaceholderText('Пароль'),
          repeatedPasswordInput = screen.getByPlaceholderText('Повторить пароль');

    await act(async() => {
        fireEvent.change(passwordInput, { target: { value: password }});
        fireEvent.change(repeatedPasswordInput, { target: { value: repeatedPassword}});
    });

    expect(passwordInput.value).toBe(password);
    expect(repeatedPasswordInput.value).toBe(repeatedPassword);

    const changeButton = screen.getByRole('button');
    await act(async() => {
        fireEvent.click(changeButton);
    });

    expect(
        document.querySelector('[data-testid="changed-successfully"]').textContent
    ).toEqual("Пароль был успешно изменен!");

    global.fetch.mockRestore();
});