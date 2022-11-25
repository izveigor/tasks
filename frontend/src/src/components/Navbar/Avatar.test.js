import React from 'react';
import { render } from '@testing-library/react';
import { fireEvent, screen } from '@testing-library/react';
import { act } from 'react-dom/test-utils';
import Avatar from './Avatar';
import {
    BrowserRouter as Router,
} from 'react-router-dom';


it("Меняем видимость меню профиля при нажатии", () => {
    const onChange = jest.fn();
    const avatar = {
        "image": "http://image",
    }

    act(() => {
        render(<Router><Avatar onChange={onChange} avatar={avatar} /></Router>);
    });

    const avatarButton = screen.getByRole('button');

    expect(
        document.querySelector('[data-testid="profile-menu"]') === null
    ).toBe(true);

    act(() => {
        fireEvent.click(avatarButton);
    });

    expect(onChange).toHaveBeenCalledTimes(1);
    expect(
        document.querySelector('[data-testid="profile-menu"]') !== null
    ).toBe(true);
});