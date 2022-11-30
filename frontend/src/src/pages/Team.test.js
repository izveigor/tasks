import React from 'react';
import { render } from '@testing-library/react';
import { act } from 'react-dom/test-utils';
import {
    BrowserRouter as Router,
} from 'react-router-dom';
import store from '../features/store';
import { Provider } from 'react-redux';
import { userUpdated } from '../features/userSlice';
import { USERS_URL_WITHOUT_SLASH } from '../features/constants';
import Team from './Team';


it('Получаем данные о команде', async() => {
    const response = {
        "name": "name",
        "image": "/image",
        "description": "description",
    };

    await act(async() => {
        store.dispatch(userUpdated({"token": "1", "isEmailConfirmed": true}));
    });

    jest.spyOn(global, "fetch").mockImplementation(() =>
        Promise.resolve({
            ok: true,
            json: () => Promise.resolve(response)
        })
    );

    await act(async() => {
        render(<Provider store={store}><Router><Team /></Router></Provider>);
    });

    expect(document.querySelector('[data-testid="team-name"]').textContent).toEqual(response.name);
    expect(document.querySelector('[data-testid="team-image"]')).toHaveAttribute('src', USERS_URL_WITHOUT_SLASH + response.image);
    expect(document.querySelector('[data-testid="team-description"]').textContent).toEqual("Описание: " + response.description);

    await act(async() => {
        store.dispatch(userUpdated({"token": null, "isEmailConfirmed": false}));
    });
    global.fetch.mockRestore();
});