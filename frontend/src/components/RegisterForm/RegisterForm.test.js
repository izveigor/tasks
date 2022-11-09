import React from 'react';
import { fireEvent, screen } from "@testing-library/react";
import { render, unmountComponentAtNode } from "react-dom";
import { act } from "react-dom/test-utils";
import RegisterForm from "./RegisterForm";


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
        render(<RegisterForm />, container);
    });

    const usernameInput = screen.getByPlaceholderText('Username');
    await act(async() => {
        fireEvent.change(usernameInput, { target: { value: inputData }});
    });
    
    expect(usernameInput.value).toBe(inputData);
    expect(
        container.querySelector("[data-testid='username-span-test']").textContent
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
        render(<RegisterForm />, container);
    });

    const emailInput = screen.getByPlaceholderText('Email');
    await act(async() => {
        fireEvent.change(emailInput, { target: { value: inputData }});
    });

    expect(emailInput.value).toBe(inputData);
    expect(
        container.querySelector("[data-testid='email-span-test']").textContent
    ).toEqual("Пользователь с таким электронным адресом уже существует!");

    global.fetch.mockRestore();
});


it("Проверяем валидацию пароля", () => {
    const passwordWithoutUpperCaseLetter = "pppassword1",
          passwordWithoutLowerCaseLetter = "PPPASSWORD1",
          passwordWithoutDigit = "PPPassword",
          passwordwithInsufficientLength = "passwor";

    act(async() => {
        render(<RegisterForm />, container);
    });

    const passwordInput = screen.getByPlaceholderText('Password');
    
    act(() => {
        fireEvent.change(passwordInput, { target: { value: passwordWithoutUpperCaseLetter }});
    });
    expect(passwordInput.value).toBe(passwordWithoutUpperCaseLetter);
    expect(
        container.querySelector("[data-testid='password-span-test']").textContent
    ).toEqual("Пароль должен содержать цифры, строчные и прописные буквы! Длина пароля должна составлять не менее 10 символов!");

    act(() => {
        fireEvent.change(passwordInput, { target: { value: passwordWithoutLowerCaseLetter }});
    });
    expect(passwordInput.value).toBe(passwordWithoutLowerCaseLetter);
    expect(
        container.querySelector("[data-testid='password-span-test']").textContent
    ).toEqual("Пароль должен содержать цифры, строчные и прописные буквы! Длина пароля должна составлять не менее 10 символов!");

    act(() => {
        fireEvent.change(passwordInput, { target: { value: passwordWithoutDigit }});
    });
    expect(passwordInput.value).toBe(passwordWithoutDigit);
    expect(
        container.querySelector("[data-testid='password-span-test']").textContent
    ).toEqual("Пароль должен содержать цифры, строчные и прописные буквы! Длина пароля должна составлять не менее 10 символов!");

    act(() => {
        fireEvent.change(passwordInput, { target: { value: passwordwithInsufficientLength }});
    });
    expect(passwordInput.value).toBe(passwordwithInsufficientLength);
    expect(
        container.querySelector("[data-testid='password-span-test']").textContent
    ).toEqual("Пароль должен содержать цифры, строчные и прописные буквы! Длина пароля должна составлять не менее 10 символов!");
});