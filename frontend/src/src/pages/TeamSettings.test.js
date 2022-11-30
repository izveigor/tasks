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
import TeamSettings from './TeamSettings';


it('Получаем текущие настройки', async() => {
    const response = {
        "image": "/image",
        "name": "name",
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
        render(<Provider store={store}><Router><TeamSettings /></Router></Provider>)
    });

    const teamImage = document.querySelector('[data-testid="team-image"]');
    const teamNameInput = document.querySelector('[data-testid="team-name-input"]');
    const teamDescriptionTextarea = document.querySelector('[data-testid="team-description-textarea"]');

    expect(teamImage).toHaveAttribute('src', USERS_URL_WITHOUT_SLASH + response.image);
    expect(teamNameInput.value).toBe(response.name);
    expect(teamDescriptionTextarea.value).toBe(response.description);

    await act(async() => {
        store.dispatch(userUpdated({"token": null, "isEmailConfirmed": false}));
    });
    global.fetch.mockRestore();
});


it('Проверяем имя команды', async() => {
    const response = {
        "image": "/image",
        "name": "name",
        "description": "description",
    };

    const existResponse = {
        "exist": true,
    };

    const newTeamName = "myTeam";

    await act(async() => {
        store.dispatch(userUpdated({"token": "1", "isEmailConfirmed": true}));
    });

    jest.spyOn(global, "fetch").mockImplementationOnce(() =>
        Promise.resolve({
            ok: true,
            json: () => Promise.resolve(response)
        })
    );

    await act(async() => {
        render(<Provider store={store}><Router><TeamSettings /></Router></Provider>)
    });

    jest.spyOn(global, "fetch").mockImplementationOnce(() =>
        Promise.resolve({
            ok: true,
            json: () => Promise.resolve(existResponse)
        })
    );

    const teamNameInput = document.querySelector('[data-testid="team-name-input"]');

    await act(async() => {
        fireEvent.change(teamNameInput, { target: { event: newTeamName}});
    });

    expect(document.querySelector('[data-testid="team-name-exist"]').textContent).toEqual("Команда с таким именем уже существует!");

    await act(async() => {
        store.dispatch(userUpdated({"token": null, "isEmailConfirmed": false}));
    });
    global.fetch.mockRestore();
});


it('Меняем настройки команды', async() => {
    const response = {
        "image": "/image",
        "name": "name",
        "description": "description",
    };

    const request = {
        "name": "name",
        "description": "description",
    };

    const fileContents = 'file contents';
    const imageName = "/image.png";
    const file = new File([fileContents], imageName, {type : 'image/png'});

    await act(async() => {
        store.dispatch(userUpdated({"token": "1", "isEmailConfirmed": true}));
    });

    jest.spyOn(global, "fetch").mockImplementation(() =>
        Promise.resolve({
            ok: true,
            json: () => Promise.resolve(request)
        })
    );

    await act(async() => {
        render(<Provider store={store}><Router><TeamSettings /></Router></Provider>)
    });

    const teamImageInput = document.querySelector('[data-testid="team-image-input"]');
    const teamNameInput = document.querySelector('[data-testid="team-name-input"]');
    const teamDescriptionTextarea = document.querySelector('[data-testid="team-description-textarea"]');

    await act(async() => {
        fireEvent.change(teamImageInput, { target: { files: [file] }});
        fireEvent.change(teamNameInput, { target: { value: request.name }})
        fireEvent.change(teamDescriptionTextarea, { target: { value: request.description }});
    });

    expect(teamImageInput.files[0].name).toBe(imageName);
    expect(teamImageInput.files.length).toBe(1);
    expect(teamNameInput.value).toBe(request.name);
    expect(teamDescriptionTextarea.value).toBe(request.description);

    const changeButton = screen.getByRole('button');

    await act(async() => {
        fireEvent.click(changeButton);
    });

    expect(document.querySelector('[data-testid="changed-successfully"]').textContent).toEqual("Настройки команды были успешно изменены!");
    
    await act(async() => {
        store.dispatch(userUpdated({"token": null, "isEmailConfirmed": false}));
    });
    global.fetch.mockRestore();
});