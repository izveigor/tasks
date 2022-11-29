import React from 'react';
import isRightPassword from './isRightPassword';


it('Проверяем валидатор пароля', () => {
    const validatedData = [
        ["password", false],
        ["Passwordd1", true],
        ["passwordd1", false],
        ["Passworddd", false],
        ["PASSWORD11", false],
        ["NEWpassword111", true],
    ];

    validatedData.map((item) => {
        expect(isRightPassword(item[0])).toBe(item[1]);
    });
});