import React from 'react';
import { act } from 'react-dom/test-utils';
import checkUsernameExist from './checkUsernameExist';



it('Проверяем данные, если пользователь существует', async() => {
    let data = {};
    const response = {
        "exist": false,
        "available": "",
    };

    jest.spyOn(global, "fetch").mockImplementation(() =>
        Promise.resolve({
            json: () => Promise.resolve(response)
        })
    );

    await act(async() => {
        data = await checkUsernameExist("username");  
    });

    expect(data).toEqual(response);  
    global.fetch.mockRestore();
});


it('Проверяем данные, если пользователь не существует', async() => {
    let data = {};
    const response = {
        "exist": true,
        "available": "username1",
    };

    jest.spyOn(global, "fetch").mockImplementation(() =>
        Promise.resolve({
            json: () => Promise.resolve(response)
        })
    );

    data = await checkUsernameExist("username");
    expect(data).toEqual(response);

    global.fetch.mockRestore();
});