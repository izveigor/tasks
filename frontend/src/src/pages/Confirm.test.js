import React from 'react';
import { screen, fireEvent, render } from '@testing-library/react';
import { act } from 'react-dom/test-utils';
import {
    BrowserRouter as Router
} from 'react-router-dom';
import store from '../features/store';
import { Provider } from 'react-redux';
import Confirm  from './Confirm';
import { userUpdated } from '../features/userSlice';

const mockUseNavigate = jest.fn();

jest.mock('react-router-dom', () => ({
    ...jest.requireActual('react-router-dom'),
    useNavigate: () => mockUseNavigate,
}));


it('Получаем количество попыток', async() => {
    store.dispatch(userUpdated({"token": "1"}));
    const response = {"available_tries": 3};
    jest.spyOn(global, "fetch").mockImplementation(() =>
        Promise.resolve({
            json: () => Promise.resolve(response)
        })
    );

    await act(async() => {
        render(<Provider store={store}><Router><Confirm /></Router></Provider>)
    });

    expect(
        document.querySelector('[data-testid="available-tries"]').textContent
    ).toEqual(`У вас осталось ${response['available_tries']} попытки!`);

    await act(async() => {
        store.dispatch(userUpdated({"token": null}));
    });
    global.fetch.mockRestore();
});


it('Если все попытки закончились', async() => {
    store.dispatch(userUpdated({"token": "1"}));
    const response = {"available_tries": 0};
    jest.spyOn(global, "fetch").mockImplementation(() =>
        Promise.resolve({
            json: () => Promise.resolve(response)
        })
    );

    await act(async() => {
        render(<Provider store={store}><Router><Confirm /></Router></Provider>)
    });

    expect(
        document.querySelector('[data-testid="available-tries"]')
    ).not.toBeInTheDocument()
    expect(mockUseNavigate).toHaveBeenCalledTimes(1);
    expect(mockUseNavigate).toHaveBeenCalledWith('..');

    await act(async() => {
        store.dispatch(userUpdated({"token": null}));
    });
    global.fetch.mockRestore();
});


it('Проверяем код успешно', async() => {
    store.dispatch(userUpdated({"token": "1"}));
    const availableTriesResponse = {"available_tries": 3};
    const confirmedResponse = {"confirmed": true};
    const code = "123456";
    jest.spyOn(global, "fetch").mockImplementationOnce(() =>
        Promise.resolve({
            json: () => Promise.resolve(availableTriesResponse)
        })
    );

    await act(async() => {
        render(<Provider store={store}><Router><Confirm /></Router></Provider>)
    });

    jest.spyOn(global, "fetch").mockImplementationOnce(() =>
        Promise.resolve({
            json: () => Promise.resolve(confirmedResponse)
        })
    );

    const inputs = screen.getAllByRole('textbox');

    await act(async() => {
        for(let i = 0; i < inputs.length; i ++) {
            fireEvent.change(inputs[i], { target: { value: code[i]}});
        }
    });

    for (let i = 0; i < inputs.length; i++) {
        expect(inputs[i].value).toBe(code[i])
    }

    const sendButton = screen.getByRole('button');

    await act(async() => {
        fireEvent.click(sendButton);
    });

    expect(mockUseNavigate).toHaveBeenCalledTimes(1);
    expect(mockUseNavigate).toHaveBeenCalledWith('../main');

    await act(async() => {
        store.dispatch(userUpdated({"token": null}));
    });
    global.fetch.mockRestore();
});


it('Проверяем код неудачно', async() => {
    store.dispatch(userUpdated({"token": "1"}));
    const availableTriesResponse = {"available_tries": 3};
    const confirmedResponse = {"confirmed": false, "available_tries": 2};
    const code = "123456";
    jest.spyOn(global, "fetch").mockImplementationOnce(() =>
        Promise.resolve({
            json: () => Promise.resolve(availableTriesResponse)
        })
    );

    await act(async() => {
        render(<Provider store={store}><Router><Confirm /></Router></Provider>)
    });

    jest.spyOn(global, "fetch").mockImplementationOnce(() =>
        Promise.resolve({
            json: () => Promise.resolve(confirmedResponse)
        })
    );

    const inputs = screen.getAllByRole('textbox');

    await act(async() => {
        for(let i = 0; i < inputs.length; i ++) {
            fireEvent.change(inputs[i], { target: { value: code[i]}});
        }
    });

    for (let i = 0; i < inputs.length; i++) {
        expect(inputs[i].value).toBe(code[i])
    }

    const sendButton = screen.getByRole('button');

    await act(async() => {
        fireEvent.click(sendButton);
    });

    expect(
        document.querySelector('[data-testid="available-tries"]').textContent
    ).toEqual(`У вас осталось ${availableTriesResponse['available_tries']-1} попытки!`);

    await act(async() => {
        store.dispatch(userUpdated({"token": null}));
    });
    global.fetch.mockRestore();
});