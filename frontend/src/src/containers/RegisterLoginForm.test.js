import React from 'react';
import { fireEvent, render } from '@testing-library/react';
import { act } from 'react-dom/test-utils';
import RegisterLoginForm from './RegisterLoginForm';
import {
    BrowserRouter as Router
} from 'react-router-dom';
import store from '../features/store';
import { Provider } from 'react-redux';


it('Переключаем форму регистрации на форму входа и наоборот', () => {
    act(() => {
        render(<Provider store={store}><Router><RegisterLoginForm /></Router></Provider>)
    });

    expect(
        document.querySelector('[data-testid="form-name"]').textContent
    ).toEqual("Форма регистрации:");
    expect(document.querySelector('[data-testid="register-form"]')).toBeInTheDocument();
    expect(document.querySelector('[data-testid="login-form"]')).not.toBeInTheDocument();

    let changeButton = document.querySelector('[data-testid="change-button"]');
    act(() => {
        fireEvent.click(changeButton);
    });

    expect(
        document.querySelector('[data-testid="form-name"]').textContent
    ).toEqual("Форма входа:");
    expect(document.querySelector('[data-testid="register-form"]')).not.toBeInTheDocument();
    expect(document.querySelector('[data-testid="login-form"]')).toBeInTheDocument();

    changeButton = document.querySelector('[data-testid="change-button"]');
    act(() => {
        fireEvent.click(changeButton);
    });

    expect(
        document.querySelector('[data-testid="form-name"]').textContent
    ).toEqual("Форма регистрации:");
    expect(document.querySelector('[data-testid="register-form"]')).toBeInTheDocument();
    expect(document.querySelector('[data-testid="login-form"]')).not.toBeInTheDocument();
});