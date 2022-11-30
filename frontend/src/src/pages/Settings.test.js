import React from 'react';
import { fireEvent, render } from '@testing-library/react';
import { act } from 'react-dom/test-utils';
import {
    BrowserRouter as Router,
} from 'react-router-dom';
import store from '../features/store';
import { Provider } from 'react-redux';
import { userUpdated } from '../features/userSlice';
import { USERS_URL_WITHOUT_SLASH } from '../features/constants';
import Settings from './Settings';


it('Проверяем изначально заполненные поля', async() => {
    const response = {
        "image": "/image",
        "job_title": "job",
        "description": "description",
        "user": {
            "first_name": "first name",
            "last_name": "last name",
        },
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
        render(<Provider store={store}><Router><Settings /></Router></Provider>);
    });

    expect(document.querySelector('[data-testid="settings-image"]')).toHaveAttribute('src', USERS_URL_WITHOUT_SLASH + response.image);
    expect(document.querySelector('[data-testid="settings-first-name-input"]').value).toEqual(response.user.first_name);
    expect(document.querySelector('[data-testid="settings-last-name-input"]').value).toEqual(response.user.last_name);
    expect(document.querySelector('[data-testid="settings-description-input"]').value).toEqual(response.description);
    expect(document.querySelector('[data-testid="settings-job-title-input"]').value).toEqual(response.job_title);

    await act(async() => {
        store.dispatch(userUpdated({"token": null, "isEmailConfirmed": false}));
    });
    global.fetch.mockRestore();
});


it('Меняем настройки', async() => {
    const fileContents = 'file contents';
    const imageName = "/image.png";
    const file = new File([fileContents], imageName, {type : 'image/png'});

    const response = {
        "image": "/image",
        "job_title": "job",
        "description": "description",
        "user": {
            "first_name": "first name",
            "last_name": "last name",
        },
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
        render(<Provider store={store}><Router><Settings /></Router></Provider>);
    });

    const settingsImageInput = document.querySelector('[data-testid="settings-image-input"]');
    const settingsFirstNameInput = document.querySelector('[data-testid="settings-first-name-input"]');
    const settingsLastNameInput = document.querySelector('[data-testid="settings-last-name-input"]');
    const settingsJobTitleInput = document.querySelector('[data-testid="settings-job-title-input"]');
    const settingsDescriptionInput = document.querySelector('[data-testid="settings-description-input"]');

    await act(async() => {
        fireEvent.change(settingsImageInput, { target: { files: [file] }});
        fireEvent.change(settingsFirstNameInput, { target: { value: response.user.first_name }});
        fireEvent.change(settingsLastNameInput, { target: { value: response.user.last_name }});
        fireEvent.change(settingsJobTitleInput, { target: { value: response.job_title }});
        fireEvent.change(settingsDescriptionInput, { target: { value: response.description }});
    });

    expect(settingsImageInput.files[0].name).toBe(imageName);
    expect(settingsImageInput.files.length).toBe(1);
    expect(settingsFirstNameInput.value).toBe(response.user.first_name);
    expect(settingsLastNameInput.value).toBe(response.user.last_name);
    expect(settingsJobTitleInput.value).toBe(response.job_title);
    expect(settingsDescriptionInput.value).toBe(response.description);

    const changeButton = document.querySelector('[data-testid="change-button"]');
    await act(async() => {
        fireEvent.click(changeButton);
    });

    expect(document.querySelector('[data-testid="changed-successfully"]').textContent).toEqual("Настройки были успешно изменены!");
    await act(async() => {
        store.dispatch(userUpdated({"token": null, "isEmailConfirmed": false}));
    });
    global.fetch.mockRestore();
});