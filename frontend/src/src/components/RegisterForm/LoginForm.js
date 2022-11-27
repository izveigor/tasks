import React, { useRef, useState } from 'react';
import { USERS_URL } from '../../features/constants';
import { useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { userUpdated } from '../../features/userSlice';


export default function LoginForm() {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const [showErrorMessage, changeShowErrorMessage] = useState(false);

    const usernameRef = useRef(null);
    const passwordRef = useRef(null);

    function login(event) {
        if(passwordRef.current.value == "" || usernameRef.current.value == "") {
            return;
        }

        fetch(USERS_URL + "login/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: usernameRef.current.value,
                password: passwordRef.current.value,
            })
        })
        .then((response) => {
            if (response.ok) {
                return response.json()
            } else {
                return null;
            }
        })
        .then((data) => {
            if (data !== null) {
                dispatch(userUpdated({"token": data.token}));
                navigate("/main");
            } else {
                changeShowErrorMessage(true);
            }
        })
        event.preventDefault();
    };

    return (
        <form data-testid="login-form" onSubmit={login}>
            <div className="grid grid-rows-4">
                <input ref={usernameRef} data-testid="username-input" type="text" className="border pl-[14px] border-gray-400 py-2 px-1 rounded-md placeholder-gray-700 mt-2 focus:outline-gray-300" placeholder="Username" required />
                <input ref={passwordRef} data-testid="password-input" type="password" className="border pl-[14px] border-gray-400 py-2 px-1 rounded-md placeholder-gray-700 mt-2 focus:outline-gray-300" placeholder="Password" required />
                {showErrorMessage && <span data-testid="login-error" className="h-[10px] py-1 text-center text-sm text-red-500">Неверное имя пользователя или пароль!</span>}
                <button type="submit" className="bg-indigo-700 py-1 px-2 rounded-md text-white mt-2 hover:bg-indigo-600">Войти</button>
            </div>
        </form>
    );
};