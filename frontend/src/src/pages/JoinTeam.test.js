import React from 'react';
import { screen, fireEvent, render } from '@testing-library/react';
import { act } from 'react-dom/test-utils';
import {
    BrowserRouter as Router,
} from 'react-router-dom';
import store from '../features/store';
import { Provider } from 'react-redux';
import JoinTeam from './JoinTeam';
import { userUpdated } from '../features/userSlice';
import { USERS_URL_WITHOUT_SLASH } from '../features/constants';


it('Предлагаем пользователю команду', async() => {
    const name = "name";
    const response = {
        "image": "/image",
        "name": "name",
    };
    store.dispatch(userUpdated({"token": "1"}));
    jest.spyOn(global, "fetch").mockImplementation(() =>
        Promise.resolve({
            ok: true,
            json: () => Promise.resolve(response)
        })
    );

    await act(async() => {
        render(<Provider store={store}><Router><JoinTeam /></Router></Provider>)
    });
    const nameInput = document.querySelector('[data-testid="name-input"]');

    await act(async() => {
        fireEvent.change(nameInput, { target: { value: name}});
    });

    expect(nameInput.value).toBe(name);
    expect(document.querySelector('[data-testid="team-information"]')).toBeInTheDocument();
    expect(document.querySelector('[data-testid="team-image"]')).toHaveAttribute('src', USERS_URL_WITHOUT_SLASH + response['image']);
    expect(document.querySelector('[data-testid="team-name"]').textContent).toEqual(response['name']);

    await act(async() => {
        store.dispatch(userUpdated({"token": null}));
    });
    global.fetch.mockRestore();
});


it('Присоединяемся к команде', async() => {
    const name = "name";
    const response = {
        "image": "/image",
        "name": "name",
    };
    store.dispatch(userUpdated({"token": "1"}));
    jest.spyOn(global, "fetch").mockImplementation(() =>
        Promise.resolve({
            ok: true,
            json: () => Promise.resolve(response)
        })
    );

    await act(async() => {
        render(<Provider store={store}><Router><JoinTeam /></Router></Provider>)
    });
    const nameInput = document.querySelector('[data-testid="name-input"]');

    await act(async() => {
        fireEvent.change(nameInput, { target: { value: name}});
    });

    await act(async() => {
        fireEvent.change(nameInput, { target: { value: name}});
    });

    expect(nameInput.value).toBe(name);
    const joinButton = screen.getByRole('button');

    await act(async() => {
        fireEvent.click(joinButton);
    });

    await act(async() => {
        store.dispatch(userUpdated({"token": null}));
    });
    global.fetch.mockRestore();
});