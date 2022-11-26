import React from 'react';
import { render } from '@testing-library/react';
import { fireEvent, screen } from '@testing-library/react';
import { act } from 'react-dom/test-utils';
import JoinOrCreateTeam from './JoinOrCreateTeam';
import {
    BrowserRouter as Router,
} from 'react-router-dom';

const mockUseNavigate = jest.fn();

jest.mock('react-router-dom', () => ({
    ...jest.requireActual('react-router-dom'),
    useNavigate: () => mockUseNavigate,
}));


it("Проверяем меню обычного пользователя", () => {
    act(() => {
        render(<Router><JoinOrCreateTeam isTeammate={false} /></Router>)
    });

    const buttonNames = [
        "Создать команду",
        "Присоединиться к команде",
    ];

    screen.getAllByRole('button').map((item, index) => {
        expect(item.textContent).toEqual(buttonNames[index])
    });

    const emptyCurrentTask = document.querySelector('[data-testid="empty-current-task"]');
    expect(emptyCurrentTask).toBeNull();
});


it("Проверяем меню участника команды", () => {
    act(() => {
        render(<Router><JoinOrCreateTeam isTeammate={true} /></Router>)
    });

    const createTeamButton = screen.queryByText("Создать команду");
    const joinTeamButton = screen.queryByText("Присоединиться к команде");

    const emptyCurrentTask = document.querySelector('[data-testid="empty-current-task"]');

    expect(createTeamButton).toBeNull();
    expect(joinTeamButton).toBeNull();
    expect(emptyCurrentTask.textContent).toEqual("Текущее задание отсутвует!");
});


it('Нажимаем на кнопку "Создать команду"', () => {
    act(() => {
        render(<Router><JoinOrCreateTeam isTeammate={false} /></Router>)
    });

    const createTeamButton = document.querySelector('[data-testid="create-team"]');

    act(() => {
        fireEvent.click(createTeamButton);
    });

    expect(mockUseNavigate).toHaveBeenCalledTimes(1)
    expect(mockUseNavigate).toHaveBeenCalledWith('../create_team');
});


it('Нажимаем на кнопку "Присоединиться"', () => {
    act(() => {
        render(<Router><JoinOrCreateTeam isTeammate={false} /></Router>)
    });

    const joinTeamButton = document.querySelector('[data-testid="join-team"]');

    act(() => {
        fireEvent.click(joinTeamButton);
    });

    expect(mockUseNavigate).toHaveBeenCalledTimes(1)
    expect(mockUseNavigate).toHaveBeenCalledWith('../join');
});


it("Проверяем меню участника команды, если у него есть ожидаемое задание", async() => {
    jest.spyOn(global, "fetch").mockImplementationOnce(() =>
        Promise.resolve({
            ok: true,
        })
    );

    await act(async() => {
        render(<Router><JoinOrCreateTeam isTeammate={true} /></Router>)
    });

    const nextTaskButton = screen.getByRole('button');
    expect(nextTaskButton.textContent).toEqual("Начать следующее задание");

    global.fetch.mockRestore();
});