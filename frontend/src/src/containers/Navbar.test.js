import React from 'react';
import { render } from '@testing-library/react';
import { act } from 'react-dom/test-utils';
import Navbar from './Navbar';
import {
    BrowserRouter as Router,
} from 'react-router-dom';
import { Provider } from 'react-redux';
import store from '../features/store';
import { userUpdated } from '../features/userSlice';


jest.mock('../components/Navbar/Bell', () => {
    return function DummyBell(props) {
      return (
        <div data-testid="bell">{props.isTeammate ? "1" : "0"}</div>
      );
    };
});


jest.mock('../components/Navbar/Menu', () => {
    return function DummyMenu(props) {
      return (
        <div data-testid="menu">{props.isTeammate ? "1": "0"}</div>
      );
    };
});


jest.mock('../components/Navbar/Avatar', () => {
    return function DummyAvatar(props) {
      return (
        <div data-testid="avatar">{props.isAdmin ? "1" : "0"}-{props.isTeammate ? "1": "0"}-{props.image}</div>
      );
    };
});


it("Показываем меню незарегистрированного пользователя", () => {
    act(() => {
        render(<Provider store={store}><Router><Navbar /></Router></Provider>);
    });

    const menu = document.querySelector('[data-testid="menu"]')
    const bell = document.querySelector('[data-testid="bell"]')
    const avatar = document.querySelector('[data-testid="avatar"]')

    expect(menu.textContent).toEqual("0");
    expect(bell === null).toBe(true);
    expect(avatar === null).toBe(true);
});


it("Показываем меню для зарегистрированного пользователя", () => {
    store.dispatch(userUpdated({"image": "1"}));
    act(() => {
        render(<Provider store={store}><Router><Navbar /></Router></Provider>);
    });

    const menu = document.querySelector('[data-testid="menu"]')
    const bell = document.querySelector('[data-testid="bell"]')
    const avatar = document.querySelector('[data-testid="avatar"]')

    const user = store.getState()["user"];

    expect(menu.textContent).toEqual("0");
    expect(bell.textContent).toEqual("0");
    expect(avatar.textContent).toEqual("0-0-" + user["image"]);

    act(() => {
        store.dispatch(userUpdated({"image": ""}));
    });
});