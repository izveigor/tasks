import React from 'react';
import { render } from '@testing-library/react';
import { fireEvent, screen } from '@testing-library/react';
import { act } from 'react-dom/test-utils';
import Task from './Task';
import {
    BrowserRouter as Router,
} from 'react-router-dom';
import { Provider } from 'react-redux';
import store from '../../features/store';


it("Проверяем props", () => {
    const props = {
        "task": {
            "title": "Название",
            "id": 1,
            "description": "Описание",
            "time": "2018-9-18T10:46:43.553472514Z"
        }
    };

    act(() => {
        render(<Task close={null} task={props["task"]} />);
    });

    expect(
        document.querySelector('[data-testid="task-title"]').textContent
    ).toEqual(props["task"]["title"] + " #" + props["task"]["id"].toString());

    expect(
        document.querySelector('[data-testid="task-description"]').textContent
    ).toEqual(props["task"]["description"]);

    expect(
        document.querySelector('[data-testid="task-time"]').textContent
    ).toEqual(props["task"]["time"].replace('T', ' ').split('.')[0]);
});