import React, { useEffect, useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { USERS_URL } from '../features/constants';
import { useSelector } from 'react-redux';
import isRightPassword from '../features/isRightPassword';


export default function ChangePassword() {
    const navigate = useNavigate();
    const token = useSelector((state) => state.user.token);
    const isEmailConfirmed = useSelector((state) => state.user.isEmailConfirmed);

    const passwordRef = useRef(null);
    const repeatedPasswordRef = useRef(null);

    const [successChanged, changeSuccessChanged] = useState(false);
    const [passwordRightState, changePasswordRightState] = useState(false);
    const [repeatedPasswordRightState, changeRepeatedPasswordRightState] = useState(false);

    function changePassword(event) {
        if (passwordRightState && repeatedPasswordRightState) {
            fetch(USERS_URL + "change_password/", {
                method: "PUT",
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': "Token " + token,
                },
                body: JSON.stringify({
                    "password": passwordRef.current.value,
                    "repeated_password": repeatedPasswordRef.current.value,
                })
            }).then((response) => {
                if(response.ok) {
                    changeSuccessChanged(true);
                }
            })
            event.preventDefault();
        }
    }

    const checkRepeatedPassword = async() => {
        if (passwordRef.current.value == repeatedPasswordRef.current.value) {
            changeRepeatedPasswordRightState(true);
        } else {
            changeRepeatedPasswordRightState(false);
        }
    };

    const changePasswordInput = async () => {
        const isRight = isRightPassword(passwordRef.current.value);
        changePasswordRightState(isRight);
    };

    useEffect(() => {
        if(token == null || !isEmailConfirmed) {
            navigate("/confirm");
        }
    }, []);

    return (
        <form onSubmit={changePassword} className="bg-white rounded-md py-2 px-2">
            <div className="text-center py-2">
                <h1 className="text-2xl">Сменить пароль:</h1>
            </div>
            <div className="px-6 mb-6 w-100 grid grid-rows-12">
                <input ref={passwordRef} onChange={async() => await changePasswordInput()} type="password" className="border pl-[14px] border-gray-400 w-100 py-2 px-1 rounded-md placeholder-gray-700 mt-2 focus:outline-gray-300" placeholder="Пароль" required />
                <input ref={repeatedPasswordRef} onChange={async() => await checkRepeatedPassword()} type="password" className="border pl-[14px] border-gray-400 w-100 py-2 px-1 rounded-md placeholder-gray-700 mt-2 focus:outline-gray-300" placeholder="Повторить пароль" required />
                {!passwordRightState && <span data-testid="wrong-password" className="h-[50px] py-1 text-center text-sm text-red-500">Пароль должен содержать цифры, строчные и прописные буквы! Длина пароля должна составлять не менее 10 символов!</span>}
                {!repeatedPasswordRightState && <span data-testid="password-not-equals-repeated-password" className="h-[50px] py-1 text-center text-sm text-red-500">Пароли не совпадают!</span>}
            </div>
            <div className="flex justify-center">
                <button type="submit" className="bg-indigo-700 py-1 px-2 w-[15em] h-[2.5em] rounded-md text-white mt-2 hover:bg-indigo-600">Сменить пароль</button>
            </div>
            {successChanged && <span data-testid="changed-successfully" className="h-[20px] py-1 text-sm text-green-500">Пароль был успешно изменен!</span>}
        </form>
    );
};