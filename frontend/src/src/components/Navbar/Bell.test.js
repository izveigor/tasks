import React from 'react';
import { render } from '@testing-library/react';
import { fireEvent, screen } from '@testing-library/react';
import { act } from 'react-dom/test-utils';
import Bell from './Bell';
import {
    BrowserRouter as Router,
} from 'react-router-dom';
import { USERS_URL_WITHOUT_SLASH } from '../../features/constants';


it("Переключаем меню уведомлений", async() => {
    const onChange = jest.fn();
    jest.spyOn(global, "fetch").mockImplementation(() =>
        Promise.resolve({
            ok: false,
            json: () => Promise.resolve([]),
        })
    );

    await act(async() => {
        render(<Router><Bell onChange={onChange} /></Router>)
    });

    const bellButton = screen.getByRole('button');

    await act(async() => {
        fireEvent.click(bellButton);
    });

    expect(onChange).toHaveBeenCalledTimes(1);
    expect(
        document.querySelector('[data-testid="empty-notifications"]').textContent
    ).toEqual("Уведомления отсутствуют!");

    global.fetch.mockRestore();
});


it("Получаем последние уведомления", async() => {
    const onChange = jest.fn();
    const fakeNotifications = [
        {
            "image": "/image1",
            "text": "Текст1",
            "time": "18:01",
        },
        {
            "image": "/image2",
            "text": "Текст2",
            "time": "18:02",
        },
        {
            "image": "/image3",
            "text": "Текст3",
            "time": "18:03",
        }
    ];

    jest.spyOn(global, "fetch").mockImplementation(() =>
        Promise.resolve({
            ok: true,
            json: () => Promise.resolve(fakeNotifications),
        })
    );

    await act(async() => {
        render(<Router><Bell onChange={onChange} /></Router>)
    });

    const bellButton = screen.getByRole('button');

    await act(async() => {
        fireEvent.click(bellButton);
    })

    expect(onChange).toHaveBeenCalledTimes(1);
    console.log(document.documentElement.innerHTML);
    [...document.querySelectorAll('[data-testid="notification-text"]')].map((item, index) => {
        expect(
            item.textContent
        ).toEqual(fakeNotifications[index]["text"] + " ")
    });

    [...document.querySelectorAll('[data-testid="notification-image"]')].map((item, index) => {
        expect(
            item
        ).toHaveAttribute('src', USERS_URL_WITHOUT_SLASH + fakeNotifications[index]["image"])
    });

    [...document.querySelectorAll('[data-testid="notification-time"]')].map((item, index) => {
        expect(
            item.textContent
        ).toEqual(fakeNotifications[index]["time"])
    });

    global.fetch.mockRestore();
});


it("Получаем количество непрочитанных уведомлений", async() => {
    const onChange = jest.fn();
    const numberUnreadNotifications = 4

    jest.spyOn(global, "fetch").mockImplementationOnce(() =>
        Promise.resolve({
            ok: true,
            json: () => Promise.resolve([]),
        })
    );

    jest.spyOn(global, "fetch").mockImplementationOnce(() =>
        Promise.resolve({
            ok: true,
            json: () => Promise.resolve(numberUnreadNotifications),
        })
    );

    await act(async() => {
        render(<Router><Bell onChange={onChange} /></Router>)
    });

    expect(
        document.querySelector('[data-testid="number-unread-notifications"]').textContent
    ).toEqual(numberUnreadNotifications.toString());

    global.fetch.mockRestore();
    const bellButton = screen.getByRole('button');

    jest.spyOn(global, "fetch").mockImplementationOnce(() =>
        Promise.resolve({
            ok: true,
        })
    );

    await act(async() => {
        fireEvent.click(bellButton);
    });

    expect(onChange).toHaveBeenCalledTimes(1);
    expect(
        document.querySelector('[data-testid="number-unread-notifications"]') === null
    ).toBe(true);

    global.fetch.mockRestore();
});
