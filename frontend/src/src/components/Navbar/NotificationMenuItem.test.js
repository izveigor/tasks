import React from 'react';
import { render } from '@testing-library/react';
import { act } from 'react-dom/test-utils';
import NotificationMenuItem from './NotificationMenuItem';
import { USERS_URL_WITHOUT_SLASH } from '../../features/constants';
import store from '../../features/store';
import { Provider } from 'react-redux';


it("Проверяем props", () => {
    const text = "Текст";
    const image = "/image";
    const time = "18:00";

    act(() => {
        render(<Provider store={store}><NotificationMenuItem text={text} image={image} time={time} /></Provider>)
    });

    expect(
        document.querySelector('[data-testid="notification-image"]')
    ).toHaveAttribute('src', USERS_URL_WITHOUT_SLASH + image);

    expect(
        document.querySelector('[data-testid="notification-text"]').textContent
    ).toEqual(text + " ");

    expect(
        document.querySelector('[data-testid="notification-time"]').textContent
    ).toEqual(time);
})