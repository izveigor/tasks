import React from 'react';
import { screen, fireEvent, render } from '@testing-library/react';
import { act } from 'react-dom/test-utils';
import {
    BrowserRouter as Router,
} from 'react-router-dom';
import store from '../features/store';
import { Provider } from 'react-redux';
import Permission from './Permission';
import { userUpdated } from '../features/userSlice';
import { USERS_URL_WITHOUT_SLASH } from '../features/constants';


it('Получаем подчиненного и руководителя', async() => {
    const names = ["supervisor", "subordinate"];
    const response = {
        "image": "/image",
        "user": {
            "first_name": "first_name",
            "last_name": "last_name",
            "username": "username",
        },
    };
    const username = "username"
    for (let i = 0; i < names.length; i++) {
        let name = names[i];
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
            render(<Provider store={store}><Router><Permission /></Router></Provider>)
        });

        const input = document.querySelector(`[data-testid="${name}-input"]`);
        await act(async() => {
            fireEvent.change(input, { target: { value: username}});
        });

        expect(input.value).toEqual(username);
        expect(document.querySelector(`[data-testid="${name}-image"]`)).toHaveAttribute('src', USERS_URL_WITHOUT_SLASH + response.image);
        expect(document.querySelector(`[data-testid="${name}-fullname"]`).textContent).toEqual(response.user.first_name + " " + response.user.last_name);
        expect(document.querySelector(`[data-testid="${name}-username"]`).textContent).toEqual(response.user.username);
    
        await act(async() => {
            store.dispatch(userUpdated({"token": null}));
        });
        global.fetch.mockRestore();
    }
});


it('Присваиваем пользователю права руководителя на другого пользователя ', async() => {
    const supervisorUsername = "supervisor";
    const subordinateUsername = "subordinate";

    const response = {
        "image": "/image",
        "user": {
            "first_name": "first_name",
            "last_name": "last_name",
            "username": "username",
        },
    };

    store.dispatch(userUpdated({"token": "1"}));
    jest.spyOn(global, "fetch").mockImplementation(() =>
        Promise.resolve({
            ok: true,
            json: () => Promise.resolve(response)
        })
    );

    await act(async() => {
        render(<Provider store={store}><Router><Permission /></Router></Provider>)
    });

    const supervisorInput = document.querySelector('[data-testid="supervisor-input"]');
    const subordinateInput = document.querySelector('[data-testid="subordinate-input"]');

    await act(async() => {
        fireEvent.change(supervisorInput, { target: { value: supervisorUsername}});
        fireEvent.change(subordinateInput, { target: { value: subordinateUsername}});
    });

    expect(supervisorInput.value).toEqual(supervisorUsername);
    expect(subordinateInput.value).toEqual(subordinateUsername);

    const permissionButton = screen.getByRole('button');

    await act(async() => {
        fireEvent.click(permissionButton);
    });

    expect(
        document.querySelector('[data-testid="set-permission-successfully"]').textContent
    ).toEqual(`Пользователь ${supervisorUsername} стал руководителем для пользователя ${subordinateUsername}!`);
    
    await act(async() => {
        store.dispatch(userUpdated({"token": null}));
    });
    global.fetch.mockRestore();
});