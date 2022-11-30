import React from 'react';
import { screen, fireEvent, render, waitFor } from '@testing-library/react';
import { act } from 'react-dom/test-utils';
import {
    BrowserRouter as Router,
} from 'react-router-dom';
import store from '../features/store';
import { Provider } from 'react-redux';
import CreateTeam from './CreateTeam';
import { userUpdated } from '../features/userSlice';
import { USERS_URL, USERS_URL_WITHOUT_SLASH } from '../features/constants';


it('Проверяем имя команды', async() => {
    const name = "name";
    const response = {"exist": true};

    store.dispatch(userUpdated({"token": "1", "isEmailConfirmed": true}));
    jest.spyOn(global, "fetch").mockImplementation(() =>
        Promise.resolve({
            ok: true,
            json: () => Promise.resolve(response)
        })
    );

    await act(async() => {
        render(<Provider store={store}><Router><CreateTeam /></Router></Provider>)
    });

    const nameInput = document.querySelector('[data-testid="name-input"]');

    await act(async() => {
        fireEvent.change(nameInput, { target: { value: name }});
    });

    expect(
        document.querySelector('[data-testid="name-exist"]').textContent
    ).toEqual("Команда с таким именем уже существует!");

    await act(async() => {
        store.dispatch(userUpdated({"token": null, "isEmailConfirmed": false}));
    });
    global.fetch.mockRestore();
});


it('Создаем команду', async() => {
    const fileContents = 'file contents';
    const imageName = "/image.png";
    const file = new File([fileContents], imageName, {type : 'image/png'});
    const request = {
        "name": "name",
        "description": "description",
        "image": file,
    };

    store.dispatch(userUpdated({"token": "1", "isEmailConfirmed": true}));

    jest.spyOn(global, "fetch").mockImplementation(() =>
        Promise.resolve({
            status: 201,
            json: () => Promise.resolve({})
        })
    );

    await act(async() => {
        render(<Provider store={store}><Router><CreateTeam /></Router></Provider>)
    });

    let showImage = document.querySelector('[data-testid="show-image"]');
    expect(showImage).toHaveAttribute('src', USERS_URL + "images/default.png");

    const nameInput = document.querySelector('[data-testid="name-input"]');
    const imageInput = document.querySelector('[data-testid="image-input"]');
    const descriptionInput = document.querySelector('[data-testid="description-input"]');

    await act(async() => {
        fireEvent.change(nameInput, { target: { value: request["name"] }});
        fireEvent.change(descriptionInput, { target: { value: request["description"] }});
        await waitFor(() => {
            fireEvent.change(imageInput, { target: { files: [request["image"]] }});
        })
    });

    expect(nameInput.value).toBe(request["name"]);
    expect(descriptionInput.value).toBe(request["description"]);
    expect(imageInput.files[0].name).toBe(imageName);
    expect(imageInput.files.length).toBe(1);

    const createButton = screen.getByRole('button');
    await act(async() => {
        fireEvent.click(createButton);
    });

    expect(document.querySelector('[data-testid="created-successfully"]').textContent).toEqual("Команда была успешно создана!");

    await act(async() => {
        store.dispatch(userUpdated({"token": null, "isEmailConfirmed": false}));
    });
    global.fetch.mockRestore();
});