import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import { act } from 'react-dom/test-utils';
import ProfileMenu from './ProfileMenu';
import {
    BrowserRouter as Router
} from 'react-router-dom';

const mockUseNavigate = jest.fn();

jest.mock('react-router-dom', () => ({
    ...jest.requireActual('react-router-dom'),
    useNavigate: () => mockUseNavigate,
}));


it("Проверяем меню обычного пользователя", () => {
    act(() => {
        render(<Router><ProfileMenu isTeammate={false} isAdmin={false} /></Router>)
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
        render(<Router><ProfileMenu isTeammate={true} isAdmin={false} /></Router>)
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
        render(<Router><ProfileMenu isTeammate={true} isAdmin={true} /></Router>)
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
    localStorage.setItem("token", "1");

    act(() => {
        render(<Router><ProfileMenu /></Router>)
    });

    const signOutButton = document.querySelector('[data-testid="sign-out"]')

    act(() => {
        fireEvent.click(signOutButton);
    });

    expect(localStorage.getItem("token") === null).toBe(true)
    expect(mockUseNavigate).toHaveBeenCalledTimes(1)
    expect(mockUseNavigate).toHaveBeenCalledWith('../confirm');
});


it("Удаляем команду", async() => {
    localStorage.setItem("token", "1");

    jest.spyOn(global, "fetch").mockImplementation(() =>
        Promise.resolve({
            ok: true,
        })
    );

    await act(async() => {
        render(<Router><ProfileMenu isTeammate={true} isAdmin={true} /></Router>)
    });

    const deleteTeam = document.querySelector('[data-testid="delete-team"]')

    await act(async() => {
        fireEvent.click(deleteTeam);
    });

    expect(localStorage.getItem("token") === null).toBe(true)
    expect(mockUseNavigate).toHaveBeenCalledTimes(1)
    expect(mockUseNavigate).toHaveBeenCalledWith('../confirm');

    global.fetch.mockRestore();
});