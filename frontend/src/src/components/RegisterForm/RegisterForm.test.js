import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { act } from 'react-dom/test-utils';
import RegisterForm from './RegisterForm';
import {
    BrowserRouter as Router
} from 'react-router-dom';
import store from '../../features/store';
import { Provider } from 'react-redux';
import { userUpdated } from '../../features/userSlice';


it('Проверяем валидацию поля "username", если он существует!', async() => {
    const inputData = 'username';
    const fakeUsernameData = {
        'exist': true,
        'available': 'username1'
    }

    jest.spyOn(global, "fetch").mockImplementation(() =>
        Promise.resolve({
            json: () => Promise.resolve(fakeUsernameData)
        })
    );

    await act(async() => {
        render(<Provider store={store}><Router><RegisterForm /></Router></Provider>);
    });

    const usernameInput = screen.getByPlaceholderText('Username');
    await act(async() => {
        fireEvent.change(usernameInput, { target: { value: inputData }});
    });
    
    expect(usernameInput.value).toBe(inputData);
    expect(
        document.querySelector("[data-testid='username-span']").textContent
    ).toEqual(`Такой пользователь уже существует! Доступное имя: "${fakeUsernameData.available}".`)

    global.fetch.mockRestore();
});


it('Проверяем валидацию поля "email", если он существует!', async() => {
    const inputData = 'email@email.com';
    const fakeEmailData = {
        'exist': true,
    };

    jest.spyOn(global, "fetch").mockImplementation(() =>
        Promise.resolve({
            json: () => Promise.resolve(fakeEmailData)
        })
    );

    await act(async() => {
        render(<Provider store={store}><Router><RegisterForm /></Router></Provider>);
    });

    const emailInput = screen.getByPlaceholderText('Email');
    await act(async() => {
        fireEvent.change(emailInput, { target: { value: inputData }});
    });

    expect(emailInput.value).toBe(inputData);
    expect(
        document.querySelector("[data-testid='email-span']").textContent
    ).toEqual("Пользователь с таким электронным адресом уже существует!");

    global.fetch.mockRestore();
});


it("Проверяем валидацию пароля", () => {
    const passwordWithoutUpperCaseLetter = "pppassword1",
          passwordWithoutLowerCaseLetter = "PPPASSWORD1",
          passwordWithoutDigit = "PPPassword",
          passwordwithInsufficientLength = "passwor";

    act(() => {
        render(<Provider store={store}><Router><RegisterForm /></Router></Provider>);
    });

    const passwordInput = screen.getByPlaceholderText('Password');
    
    act(() => {
        fireEvent.change(passwordInput, { target: { value: passwordWithoutUpperCaseLetter }});
    });
    expect(passwordInput.value).toBe(passwordWithoutUpperCaseLetter);
    expect(
        document.querySelector("[data-testid='password-span']").textContent
    ).toEqual("Пароль должен содержать цифры, строчные и прописные буквы! Длина пароля должна составлять не менее 10 символов!");

    act(() => {
        fireEvent.change(passwordInput, { target: { value: passwordWithoutLowerCaseLetter }});
    });
    expect(passwordInput.value).toBe(passwordWithoutLowerCaseLetter);
    expect(
        document.querySelector("[data-testid='password-span']").textContent
    ).toEqual("Пароль должен содержать цифры, строчные и прописные буквы! Длина пароля должна составлять не менее 10 символов!");

    act(() => {
        fireEvent.change(passwordInput, { target: { value: passwordWithoutDigit }});
    });
    expect(passwordInput.value).toBe(passwordWithoutDigit);
    expect(
        document.querySelector("[data-testid='password-span']").textContent
    ).toEqual("Пароль должен содержать цифры, строчные и прописные буквы! Длина пароля должна составлять не менее 10 символов!");

    act(() => {
        fireEvent.change(passwordInput, { target: { value: passwordwithInsufficientLength }});
    });
    expect(passwordInput.value).toBe(passwordwithInsufficientLength);
    expect(
        document.querySelector("[data-testid='password-span']").textContent
    ).toEqual("Пароль должен содержать цифры, строчные и прописные буквы! Длина пароля должна составлять не менее 10 символов!");
});

const mockUseNavigate = jest.fn();

jest.mock('react-router-dom', () => ({
    ...jest.requireActual('react-router-dom'),
    useNavigate: () => mockUseNavigate,
}));


it("Регистрируем пользователя", async() => {
    const response = {"token": "1"};
    jest.spyOn(global, "fetch").mockImplementation(() =>
        Promise.resolve({
            json: () => Promise.resolve(response),
        })
    );

    await act(async() => {
        render(<Provider store={store}><Router><RegisterForm /></Router></Provider>)
    });

    const inputData = {
        "first_name": "first name",
        "last_name": "last name",
        "username": "username",
        "email": "email",
        "password": "Password11",
    }

    const firstNameInput = document.querySelector('[data-testid="first-name-input"]');
    const lastNameInput = document.querySelector('[data-testid="last-name-input"]');

    const usernameInput = document.querySelector('[data-testid="username-input"]');
    const emailInput = document.querySelector('[data-testid="email-input"]');
    const passwordInput = document.querySelector('[data-testid="password-input"]');

    const registerButton = screen.getByRole('button');

    await act(async() => {
        fireEvent.change(firstNameInput, { target: { value: inputData["first_name"]}});
        fireEvent.change(lastNameInput, { target: { value: inputData["last_name"]}});

        fireEvent.change(usernameInput, { target: { value: inputData["username"]}});
        fireEvent.change(emailInput, { target: { value: inputData["email"]}});
        fireEvent.change(passwordInput, { target: { value: inputData["password"]}});
    });

    await act(async() => {
        fireEvent.click(registerButton);
    });

    expect(store.getState()["user"]["token"]).toEqual(response["token"]);
    expect(mockUseNavigate).toHaveBeenCalledTimes(1);
    expect(mockUseNavigate).toHaveBeenCalledWith('/confirm');

    await act(async() => {
        store.dispatch(userUpdated({"token": null}));
    });
    global.fetch.mockRestore();
});