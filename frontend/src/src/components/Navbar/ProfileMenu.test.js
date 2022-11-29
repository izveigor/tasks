import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import { act } from 'react-dom/test-utils';
import ProfileMenu from './ProfileMenu';
import {
    BrowserRouter as Router
} from 'react-router-dom';
import { Provider } from 'react-redux';
import store from '../../features/store';
import { userUpdated } from '../../features/userSlice';

const mockUseNavigate = jest.fn();

jest.mock('react-router-dom', () => ({
    ...jest.requireActual('react-router-dom'),
    useNavigate: () => mockUseNavigate,
}));


it("Проверяем меню обычного пользователя", () => {
    act(() => {
        render(<Provider store={store}><Router><ProfileMenu isTeammate={false} isAdmin={false} /></Router></Provider>)
    });

    const names = [
        "Мой профиль",
        "Настройки",
        "Выйти",
    ];

    screen.getAllByRole('link').map((item, index) => {
        expect(item.textContent).toEqual(names[index]);
    });
});


it("Проверяем меню участника команды", () => {
    act(() => {
        render(<Provider store={store}><Router><ProfileMenu isTeammate={true} isAdmin={false} /></Router></Provider>)
    });

    const names = [
        "Мой профиль",
        "Настройки",
        "Выйти",
        "Выйти из команды"
    ];

    expect(screen.getByRole('separator')).toBeInTheDocument();
    screen.getAllByRole('link').map((item, index) => {
        expect(item.textContent).toEqual(names[index]);
    });
});

it("Проверяем меню админа", () => {
    act(() => {
        render(<Provider store={store}><Router><ProfileMenu isTeammate={true} isAdmin={true} /></Router></Provider>)
    });

    const names = [
        "Мой профиль",
        "Настройки",
        "Выйти",
        "Дать разрешение",
        "Настройки команды",
        "Удалить команду",
    ];

    expect(screen.getByRole('separator')).toBeInTheDocument();
    screen.getAllByRole('link').map((item, index) => {
        expect(item.textContent).toEqual(names[index]);
    });
});


it("Выходим из аккаунта", () => {
    store.dispatch(userUpdated({"token": "1"}))
    act(() => {
        render(<Provider store={store}><Router><ProfileMenu /></Router></Provider>)
    });

    const signOutButton = document.querySelector('[data-testid="sign-out"]')

    act(() => {
        fireEvent.click(signOutButton);
    });

    expect(store.getState()["user"]["token"] === null).toBe(true)
    expect(mockUseNavigate).toHaveBeenCalledTimes(1)
    expect(mockUseNavigate).toHaveBeenCalledWith('../confirm');
    act(() => {
        store.dispatch(userUpdated({"token": null}))
    });
});


it("Удаляем команду", async() => {
    jest.spyOn(global, "fetch").mockImplementation(() =>
        Promise.resolve({
            ok: true,
        })
    );

    await act(async() => {
        render(<Provider store={store}><Router><ProfileMenu isTeammate={true} isAdmin={true} /></Router></Provider>)
    });

    const deleteTeam = document.querySelector('[data-testid="delete-team"]')

    await act(async() => {
        fireEvent.click(deleteTeam);
    });

    expect(mockUseNavigate).toHaveBeenCalledTimes(1)
    expect(mockUseNavigate).toHaveBeenCalledWith('../confirm');

    global.fetch.mockRestore();
});