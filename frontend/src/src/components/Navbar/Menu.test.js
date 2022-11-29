import React from 'react';
import { render } from '@testing-library/react';
import { fireEvent, screen } from '@testing-library/react';
import { act } from 'react-dom/test-utils';
import Menu from './Menu';
import {
    BrowserRouter as Router,
} from 'react-router-dom';
import { Provider } from 'react-redux';
import store from '../../features/store';
import { userUpdated } from '../../features/userSlice';


it("Показываем меню для незарегистрированного пользователя", () => {
    const names = [
        "Главная",
        "О нас",
    ];

    act(() => {
        render(<Provider store={store}><Router><Menu isTeammate={false} /></Router></Provider>);
    });

    const links = screen.getAllByRole('link');
    links.map((item, index) => {
        expect(item.textContent).toEqual(names[index]);
    });

    expect(links[0]).toHaveAttribute('href', '/');
});


it("Показываем меню для зарегистрированного пользователя", () => {
    const names = [
        "Главная",
        "О нас",
    ];

    store.dispatch(userUpdated({"token": "1"}));
    act(() => {
        render(<Provider store={store}><Router><Menu isTeammate={false} /></Router></Provider>);
    });

    const links = screen.getAllByRole('link')
    links.map((item, index) => {
        expect(item.textContent).toEqual(names[index]);
    });

    expect(links[0]).toHaveAttribute('href', '/main');
    act(() => {
        store.dispatch(userUpdated({"token": null}));
    });
});


it("Показываем меню для участника команды", () => {
    const names = [
        "Главная",
        "Команда",
        "О нас",
    ];

    store.dispatch(userUpdated({"token": "1"}));
    act(() => {
        render(<Provider store={store}><Router><Menu isTeammate={true} /></Router></Provider>);
    });

    const links = screen.getAllByRole('link')
    links.map((item, index) => {
        expect(item.textContent).toEqual(names[index]);
    });

    expect(links[0]).toHaveAttribute('href', '/main');
    act(() => {
        store.dispatch(userUpdated({"token": null}));
    });
});


it("Показываем меню для создателя заданий", () => {
    const names = [
        "Главная",
        "Команда",
        "О нас",
        "Создать задание",
    ];

    store.dispatch(userUpdated({"token": "1", "isCreator": true}));
    act(() => {
        render(<Provider store={store}><Router><Menu isTeammate={true} /></Router></Provider>);
    });

    const links = screen.getAllByRole('link')
    links.map((item, index) => {
        expect(item.textContent).toEqual(names[index]);
    });

    expect(links[0]).toHaveAttribute('href', '/main');
    act(() => {
        store.dispatch(userUpdated({"token": null, "isCreator": false}));
    });
});