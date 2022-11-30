import React from 'react';
import { fireEvent, render } from '@testing-library/react';
import { act } from 'react-dom/test-utils';
import {
    BrowserRouter as Router
} from 'react-router-dom';
import store from '../features/store';
import { Provider } from 'react-redux';
import CreateTask from './CreateTask';
import { userUpdated } from '../features/userSlice';
import { USERS_URL_WITHOUT_SLASH } from '../features/constants';


it('Добавляем и удаляем ids предшествующих и последующих заданий', () => {
    const names = ['previous', 'subsequent'];

    names.forEach((name) => {
        const ids = [1];
        act(() => {
            store.dispatch(userUpdated({"token": "1", "isCreator": true}));
        });

        act(() => {
            render(<Provider store={store}><Router><CreateTask /></Router></Provider>)
        });

        const button = document.querySelector(`[data-testid="${name}-button"]`);
        const input = document.querySelector(`[data-testid="${name}-input"]`);

        ids.forEach((id) => {
            act(() => {
                fireEvent.change(input, { target: { value: id}});
            });

            expect(input.value).toBe(id.toString());

            act(() => {
                fireEvent.click(button);
            });
        });

        const badges = document.querySelectorAll(`[data-testid="${name}-badge"]`);
        for(let i = 0; i < badges.length; i++) {
            expect(badges[i].textContent).toEqual(ids[i] + " ");
        }

        badges.forEach(badge => {
            act(() => {
                fireEvent.click(badge.querySelector('button'));
            });
        })

        expect(document.querySelector(`[data-testid="${name}-badge"]`)).not.toBeInTheDocument();

        act(() => {
            store.dispatch(userUpdated({"token": null, "isCreator": false}))
            document.body.innerHTML = "";
        });
    })
});


it('Находим подчиненного', async() => {
    const response = {
        "image": "/image1",
        "user": {
            "first_name": "first name",
            "last_name": "last name",
            "username": "username",
        }
    };

    store.dispatch(userUpdated({"token": "1", "isCreator": true}));

    jest.spyOn(global, "fetch").mockImplementation(() =>
        Promise.resolve({
            ok: true,
            json: () => Promise.resolve(response)
        })
    );

    await act(async() => {
        render(<Provider store={store}><Router><CreateTask /></Router></Provider>)
    });

    const employeeInput = document.querySelector('[data-testid="employee-input"]');

    await act(async() => {
        fireEvent.change(employeeInput, { target: { value: response['user']['username']}});
    });

    expect(document.querySelector('[data-testid="employee-data"]')).toBeInTheDocument();
    expect(document.querySelector('[data-testid="employee-image"]')).toHaveAttribute('src', USERS_URL_WITHOUT_SLASH + response.image);
    expect(document.querySelector('[data-testid="employee-fullname"]').textContent).toEqual(response.user.first_name + " " + response.user.last_name);
    expect(document.querySelector('[data-testid="employee-username"]').textContent).toEqual(response.user.username);

    await act(async() => {
        store.dispatch(userUpdated({"token": null, "isCreator": false}))
    });

    global.fetch.mockRestore();
});


it('Создаем задание', async() => {
    store.dispatch(userUpdated({"token": "1", "isCreator": true}));

    const inputData = {
        "employee": "employee",
        "title": "title",
        "time": "18:00",
        "description": "description",
        "previousId": 1,
        "subsequentId": 2,
    };

    jest.spyOn(global, "fetch").mockImplementation(() =>
        Promise.resolve({
            status: 201,
        })
    );

    await act(async() => {
        render(<Provider store={store}><Router><CreateTask /></Router></Provider>)
    });

    const employeeInput = document.querySelector('[data-testid="employee-input"]');
    const titleInput = document.querySelector('[data-testid="title-input"]');
    const timeInput = document.querySelector('[data-testid="time-input"]');

    const previousInput = document.querySelector('[data-testid="previous-input"]');
    const previousButton = document.querySelector('[data-testid="previous-button"]');

    const subsequentInput = document.querySelector('[data-testid="subsequent-input"]');
    const subsequentButton = document.querySelector('[data-testid="subsequent-button"]');

    const descriptionTextarea = document.querySelector('[data-testid="description-textarea"]');

    await act(async() => {
        fireEvent.change(employeeInput, { target: { value: inputData['employee']}});
        fireEvent.change(titleInput, { target: { value: inputData['title']}});
        fireEvent.change(timeInput, { target: { value: inputData['time']}});
        fireEvent.change(descriptionTextarea, { target: { value: inputData['description']}});
    
        fireEvent.change(previousInput, { target: { value: inputData['previousId']}});
        fireEvent.change(subsequentInput, { target: { value: inputData['subsequentId']}});
    });

    expect(employeeInput.value).toBe(inputData['employee']);
    expect(titleInput.value).toBe(inputData['title']);
    expect(timeInput.value).toBe(inputData['time']);
    expect(descriptionTextarea.value).toBe(inputData['description']);
    
    expect(previousInput.value).toBe(inputData['previousId'].toString());
    expect(subsequentInput.value).toBe(inputData['subsequentId'].toString());

    await act(async() => {
        fireEvent.click(previousButton);
        fireEvent.click(subsequentButton);
    });

    expect(document.querySelector(
        '[data-testid="previous-badge"]'
    ).textContent).toEqual(inputData['previousId'] + " ");
    expect(document.querySelector(
        '[data-testid="subsequent-badge"]'
    ).textContent).toEqual(inputData['subsequentId'] + " ");

    const createButton = document.querySelector('[data-testid="create-button"]');
    await act(async() => {
        fireEvent.click(createButton);
    });

    expect(document.querySelector('[data-testid="created-successfully"]').textContent).toEqual("Задание успешно создано!");
    await act(async() => {
        store.dispatch(userUpdated({"token": null, "isCreator": false}))
    });

    global.fetch.mockRestore();
});