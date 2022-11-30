import React from 'react';
import { screen, fireEvent, render } from '@testing-library/react';
import { act } from 'react-dom/test-utils';
import {
    BrowserRouter as Router,
} from 'react-router-dom';
import store from '../features/store';
import { Provider } from 'react-redux';
import { userUpdated } from '../features/userSlice';
import { USERS_URL_WITHOUT_SLASH } from '../features/constants';
import Profile from './Profile';


it('Получаем данные из профиля', async() => {
    const response = {
        "image": "/image",
        "job_title": "job",
        "description": "description",
        "user": {
            "first_name": "first name",
            "last_name": "last name",
            "username": "username",
        },
    };

    await act(async() => {
        store.dispatch(userUpdated({"token": "1"}));
    });

    jest.spyOn(global, "fetch").mockImplementation(() =>
        Promise.resolve({
            ok: true,
            json: () => Promise.resolve(response)
        })
    );

    await act(async() => {
        render(<Provider store={store}><Router><Profile /></Router></Provider>);
    });

    expect(document.querySelector('[data-testid="profile-fullname"]').textContent).toEqual(response.user.first_name + " " + response.user.last_name + " (" + response.user.username + ")");
    expect(document.querySelector('[data-testid="profile-image"]')).toHaveAttribute('src', USERS_URL_WITHOUT_SLASH + response.image);
    expect(document.querySelector('[data-testid="profile-job-title"]').textContent).toEqual("Должность: " + response.job_title);
    expect(document.querySelector('[data-testid="profile-description"]').textContent).toEqual("Описание: " + response.description);
});