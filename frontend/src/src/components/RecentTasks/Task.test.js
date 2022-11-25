import React from 'react';
import { render } from '@testing-library/react';
import { act } from 'react-dom/test-utils';
import Task from './Task';
import { USERS_URL_WITHOUT_SLASH } from '../../features/constants';


it("Проверяем props", () => {
    const propsData = 
    [
        {
            'title': 'Сделать отчет о страусах',
            'id': 1,
            'time': '20 минут',
            'image': 'https://image',
            'status': 'Успешно',
        }, 
        {
            'title': 'Сделать отчет о воробьях',
            'id': 2,
            'time': '30 минут',
            'image': 'https://image2',
            'status': 'Обработка',
        }, 
        {
            'title': 'Сделать отчет о сороках',
            'id': 3,
            'time': '40 минут',
            'image': 'https://image3',
            'status': 'Закрыто',
        },
    ];

    propsData.forEach((data) => {
        act(() => {
            render(<Task title={data.title}
                id={data.id}
                time={data.time}
                image={data.image}
                status={data.status}
            />);
        });

        expect(
            document.querySelector("[data-testid='task-name']").textContent
        ).toEqual(data.title + " #" + data.id.toString());
        expect(
            document.querySelector("[data-testid='task-time']").textContent
        ).toEqual(data.time);
        expect(
            document.querySelector("[data-testid='task-image']")
        ).toHaveAttribute('src', USERS_URL_WITHOUT_SLASH + data.image);
        expect(
            document.querySelector("[data-testid='task-status']").textContent
        ).toEqual(data.status);

        document.body.innerHTML = "";
    });
});